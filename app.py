import os
from flask import Flask, request, jsonify, send_from_directory, redirect, url_for, session
import csv
import time
from cryptography.fernet import Fernet

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

# File paths for CSV files
STUDENT_FILE = 'students.csv'
COURSE_FILE = 'courses.csv'
PROFESSOR_FILE = 'professors.csv'
LOGIN_FILE = 'login.csv'
GRADES_FILE = 'grades.csv'

# Generate a key for encryption (store this securely in a real application)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to initialize CSV files with headers if they don't exist
def initialize_csv(file_path, headers):
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()

# Initialize CSV files
initialize_csv(STUDENT_FILE, ['Email_address', 'First_name', 'Last_name', 'Course.id', 'grades', 'Marks'])
initialize_csv(COURSE_FILE, ['Course_id', 'Course_name', 'Description'])
initialize_csv(PROFESSOR_FILE, ['Professor_id', 'Professor_Name', 'Rank', 'Course.id'])
initialize_csv(GRADES_FILE, ['Grade_id', 'Grade', 'Marks_range'])
initialize_csv(LOGIN_FILE, ['User_id', 'Password', 'Role'])

# Helper function to read CSV files
def read_csv(file_path):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Helper function to write to CSV files
def write_csv(file_path, data, fieldnames):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# Encrypt password
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode()).decode()

# Decrypt password
def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

# Serve the login/registration page
@app.route('/')
def index():
    return send_from_directory('.', 'login.html')

# Serve the dashboard page (after successful login)
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        return send_from_directory('.', 'dashboard.html')
    else:
        return redirect(url_for('index'))

# Serve static files (CSS, JS, etc.)
@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# Register a new user (with password encryption)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    login_data = read_csv(LOGIN_FILE)
    
    # Check if the user already exists
    if any(user['User_id'] == data['User_id'] for user in login_data):
        return jsonify({"message": "User already exists!"}), 400
    
    # Encrypt the password
    data['Password'] = encrypt_password(data['Password'])
    
    # Add the new user
    login_data.append(data)
    write_csv(LOGIN_FILE, login_data, fieldnames=data.keys())
    return jsonify({"message": "User registered successfully!"}), 201

# Login a user (with password decryption)
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    login_data = read_csv(LOGIN_FILE)
    
    # Find the user
    user = next((user for user in login_data if user['User_id'] == data['User_id']), None)
    
    if user and data['Password'] == decrypt_password(user['Password']):
        session['user_id'] = user['User_id']  # Store user ID in session
        return jsonify({"message": "Login successful!", "redirect": url_for('dashboard')}), 200
    else:
        return jsonify({"message": "Invalid credentials!"}), 401

# Logout a user
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    return jsonify({"message": "Logged out successfully!", "redirect": url_for('index')}), 200

# Add a new student
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json
    students = read_csv(STUDENT_FILE)
    students.append(data)
    write_csv(STUDENT_FILE, students, fieldnames=data.keys())
    return jsonify({"message": "Student added successfully!"}), 201

# Delete a student
@app.route('/delete_student/<email>', methods=['DELETE'])
def delete_student(email):
    students = read_csv(STUDENT_FILE)
    students = [student for student in students if student['Email_address'] != email]
    write_csv(STUDENT_FILE, students, fieldnames=students[0].keys() if students else [])
    return jsonify({"message": "Student deleted successfully!"}), 200

# Modify a student
@app.route('/modify_student/<email>', methods=['PUT'])
def modify_student(email):
    data = request.json
    students = read_csv(STUDENT_FILE)
    for student in students:
        if student['Email_address'] == email:
            student.update(data)
            break
    write_csv(STUDENT_FILE, students, fieldnames=students[0].keys())
    return jsonify({"message": "Student modified successfully!"}), 200

# Search for a student
@app.route('/search_student/<email>', methods=['GET'])
def search_student(email):
    students = read_csv(STUDENT_FILE)
    start_time = time.time()
    student = next((student for student in students if student['Email_address'] == email), None)
    end_time = time.time()
    if student:
        return jsonify({"student": student, "time_taken": end_time - start_time}), 200
    else:
        return jsonify({"message": "Student not found!"}), 404

# Sort students by marks
@app.route('/sort_students_by_marks', methods=['GET'])
def sort_students_by_marks():
    students = read_csv(STUDENT_FILE)
    start_time = time.time()
    sorted_students = sorted(students, key=lambda x: int(x['Marks']), reverse=True)
    end_time = time.time()
    return jsonify({"sorted_students": sorted_students, "time_taken": end_time - start_time}), 200

# Show all students
@app.route('/students', methods=['GET'])
def show_all_students():
    students = read_csv(STUDENT_FILE)
    return jsonify(students), 200

# Show all professors
@app.route('/professors', methods=['GET'])
def show_all_professors():
    professors = read_csv(PROFESSOR_FILE)
    return jsonify(professors), 200

# Show all courses
@app.route('/courses', methods=['GET'])
def show_all_courses():
    courses = read_csv(COURSE_FILE)
    return jsonify(courses), 200

# Get average marks for a course
@app.route('/average_marks/<course_id>', methods=['GET'])
def average_marks(course_id):
    students = read_csv(STUDENT_FILE)
    course_students = [student for student in students if student['Course.id'] == course_id]
    if not course_students:
        return jsonify({"message": "No students found for this course!"}), 404
    total_marks = sum(int(student['Marks']) for student in course_students)
    average = total_marks / len(course_students)
    return jsonify({"average_marks": average}), 200

# Add a new professor
@app.route('/add_professor', methods=['POST'])
def add_professor():
    data = request.json
    professors = read_csv(PROFESSOR_FILE)
    professors.append(data)
    write_csv(PROFESSOR_FILE, professors, fieldnames=data.keys())
    return jsonify({"message": "Professor added successfully!"}), 201

# Delete a professor
@app.route('/delete_professor/<professor_id>', methods=['DELETE'])
def delete_professor(professor_id):
    professors = read_csv(PROFESSOR_FILE)
    professors = [professor for professor in professors if professor['Professor_id'] != professor_id]
    write_csv(PROFESSOR_FILE, professors, fieldnames=professors[0].keys() if professors else [])
    return jsonify({"message": "Professor deleted successfully!"}), 200

# Modify a professor
@app.route('/modify_professor/<professor_id>', methods=['PUT'])
def modify_professor(professor_id):
    data = request.json
    professors = read_csv(PROFESSOR_FILE)
    for professor in professors:
        if professor['Professor_id'] == professor_id:
            professor.update(data)
            break
    write_csv(PROFESSOR_FILE, professors, fieldnames=professors[0].keys())
    return jsonify({"message": "Professor modified successfully!"}), 200

# Add a new course
@app.route('/add_course', methods=['POST'])
def add_course():
    data = request.json
    courses = read_csv(COURSE_FILE)
    courses.append(data)
    write_csv(COURSE_FILE, courses, fieldnames=data.keys())
    return jsonify({"message": "Course added successfully!"}), 201

# Delete a course
@app.route('/delete_course/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    courses = read_csv(COURSE_FILE)
    courses = [course for course in courses if course['Course_id'] != course_id]
    write_csv(COURSE_FILE, courses, fieldnames=courses[0].keys() if courses else [])
    return jsonify({"message": "Course deleted successfully!"}), 200

# Modify a course
@app.route('/modify_course/<course_id>', methods=['PUT'])
def modify_course(course_id):
    data = request.json
    courses = read_csv(COURSE_FILE)
    for course in courses:
        if course['Course_id'] == course_id:
            course.update(data)
            break
    write_csv(COURSE_FILE, courses, fieldnames=courses[0].keys())
    return jsonify({"message": "Course modified successfully!"}), 200

# Add a new grade
@app.route('/add_grade', methods=['POST'])
def add_grade():
    data = request.json
    grades = read_csv(GRADES_FILE)
    grades.append(data)
    write_csv(GRADES_FILE, grades, fieldnames=data.keys())
    return jsonify({"message": "Grade added successfully!"}), 201

# Delete a grade
@app.route('/delete_grade/<grade_id>', methods=['DELETE'])
def delete_grade(grade_id):
    grades = read_csv(GRADES_FILE)
    grades = [grade for grade in grades if grade['Grade_id'] != grade_id]
    write_csv(GRADES_FILE, grades, fieldnames=grades[0].keys() if grades else [])
    return jsonify({"message": "Grade deleted successfully!"}), 200

# Modify a grade
@app.route('/modify_grade/<grade_id>', methods=['PUT'])
def modify_grade(grade_id):
    data = request.json
    grades = read_csv(GRADES_FILE)
    for grade in grades:
        if grade['Grade_id'] == grade_id:
            grade.update(data)
            break
    write_csv(GRADES_FILE, grades, fieldnames=grades[0].keys())
    return jsonify({"message": "Grade modified successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
import csv
import random

# Function to generate random student data
def generate_student_data(num_records):
    students = []
    for i in range(1, num_records + 1):
        email = f"student{i}@example.com"
        first_name = f"Student{i}"
        last_name = f"Last{i}"
        course_id = random.choice(["DATA200", "DATA300", "DATA400"])
        grade = random.choice(["A", "B", "C", "D", "F"])
        marks = random.randint(50, 100)  # Random marks between 50 and 100
        students.append([email, first_name, last_name, course_id, grade, marks])
    return students

# Write student data to CSV
def write_to_csv(filename, data):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Email_address', 'First_name', 'Last_name', 'Course.id', 'grades', 'Marks'])
        writer.writerows(data)

# Generate 1000 student records
num_records = 1000
students = generate_student_data(num_records)

# Write to students.csv
write_to_csv('students.csv', students)

print(f"{num_records} student records generated and saved to students.csv")
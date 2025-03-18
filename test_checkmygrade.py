import unittest
import csv
import time
from app import app  # Import your Flask app

class TestCheckMyGrade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the Flask test client
        cls.app = app.test_client()
        cls.app.testing = True

        # Initialize CSV files for testing
        cls.student_file = 'students.csv'
        cls.course_file = 'courses.csv'
        cls.professor_file = 'professors.csv'

        # Clear existing data in CSV files (except students.csv, which has 1000 records)
        with open(cls.course_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Course_id', 'Course_name', 'Description', 'Credits'])

        with open(cls.professor_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Professor_id', 'Professor_Name', 'Email', 'Rank', 'Course.id'])

    def test_add_student(self):
        # Test adding a student
        response = self.app.post('/add_student', json={
            'Email_address': 'john@example.com',
            'First_name': 'John',
            'Last_name': 'Doe',
            'Course.id': 'DATA200',
            'grades': 'A',
            'Marks': '95'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Student added successfully!', response.get_json()['message'])

    def test_delete_student(self):
        # Add a student first
        self.app.post('/add_student', json={
            'Email_address': 'jane@example.com',
            'First_name': 'Jane',
            'Last_name': 'Smith',
            'Course.id': 'DATA200',
            'grades': 'B',
            'Marks': '85'
        })

        # Test deleting the student
        response = self.app.delete('/delete_student/jane@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Student deleted successfully!', response.get_json()['message'])

    def test_modify_student(self):
        # Add a student first
        self.app.post('/add_student', json={
            'Email_address': 'alice@example.com',
            'First_name': 'Alice',
            'Last_name': 'Johnson',
            'Course.id': 'DATA200',
            'grades': 'C',
            'Marks': '75'
        })

        # Test modifying the student
        response = self.app.put('/modify_student/alice@example.com', json={
            'First_name': 'Alice',
            'Last_name': 'Brown',
            'Course.id': 'DATA200',
            'grades': 'B',
            'Marks': '80'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Student modified successfully!', response.get_json()['message'])

    def test_search_student_with_1000_records(self):
        # Test searching for a student in 1000 records
        start_time = time.time()
        response = self.app.get('/search_student/student500@example.com')
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        self.assertIn('Student500', response.get_json()['student']['First_name'])
        print(f"Time taken to search in 1000 records: {end_time - start_time} seconds")

    def test_sort_students_by_marks_with_1000_records(self):
        # Test sorting students by marks in 1000 records
        start_time = time.time()
        response = self.app.get('/sort_students_by_marks')
        end_time = time.time()
        self.assertEqual(response.status_code, 200)
        
        # Check if the first student has higher marks than the second
        sorted_students = response.get_json()['sorted_students']
        self.assertGreaterEqual(int(sorted_students[0]['Marks']), int(sorted_students[1]['Marks']))
        print(f"Time taken to sort 1000 records: {end_time - start_time} seconds")

    def test_add_course(self):
        # Test adding a course
        response = self.app.post('/add_course', json={
            'Course_id': 'DATA200',
            'Course_name': 'Data Science',
            'Description': 'Introduction to Data Science',
            'Credits': '3'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Course added successfully!', response.get_json()['message'])

    def test_delete_course(self):
        # Add a course first
        self.app.post('/add_course', json={
            'Course_id': 'DATA300',
            'Course_name': 'Machine Learning',
            'Description': 'Advanced Machine Learning',
            'Credits': '4'
        })

        # Test deleting the course
        response = self.app.delete('/delete_course/DATA300')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Course deleted successfully!', response.get_json()['message'])

    def test_modify_course(self):
        # Add a course first
        self.app.post('/add_course', json={
            'Course_id': 'DATA400',
            'Course_name': 'Deep Learning',
            'Description': 'Introduction to Deep Learning',
            'Credits': '4'
        })

        # Test modifying the course
        response = self.app.put('/modify_course/DATA400', json={
            'Course_name': 'Advanced Deep Learning',
            'Description': 'Advanced topics in Deep Learning',
            'Credits': '5'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Course modified successfully!', response.get_json()['message'])

    def test_add_professor(self):
        # Test adding a professor
        response = self.app.post('/add_professor', json={
            'Professor_id': 'prof1@example.com',
            'Professor_Name': 'Dr. Smith',
            'Email': 'smith@example.com',
            'Rank': 'Senior Professor',
            'Course.id': 'DATA200'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Professor added successfully!', response.get_json()['message'])

    def test_delete_professor(self):
        # Add a professor first
        self.app.post('/add_professor', json={
            'Professor_id': 'prof2@example.com',
            'Professor_Name': 'Dr. Johnson',
            'Email': 'johnson@example.com',
            'Rank': 'Associate Professor',
            'Course.id': 'DATA200'
        })

        # Test deleting the professor
        response = self.app.delete('/delete_professor/prof2@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Professor deleted successfully!', response.get_json()['message'])

    def test_modify_professor(self):
        # Add a professor first
        self.app.post('/add_professor', json={
            'Professor_id': 'prof3@example.com',
            'Professor_Name': 'Dr. Brown',
            'Email': 'brown@example.com',
            'Rank': 'Assistant Professor',
            'Course.id': 'DATA200'
        })

        # Test modifying the professor
        response = self.app.put('/modify_professor/prof3@example.com', json={
            'Professor_Name': 'Dr. Brown',
            'Email': 'brown@example.com',
            'Rank': 'Senior Professor',
            'Course.id': 'DATA200'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Professor modified successfully!', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
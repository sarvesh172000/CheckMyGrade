# CheckMyGrade

CheckMyGrade is a Python-based application for managing student grades, courses, and professors. It provides functionalities such as adding, deleting, modifying, and searching records, as well as generating reports and statistics.

---

## Features

- **Student Management**:
  - Add, delete, and modify student records.
  - Search for students by email.
  - Sort students by marks.

- **Course Management**:
  - Add, delete, and modify course records.
  - View all courses.

- **Professor Management**:
  - Add, delete, and modify professor records.
  - View all professors.

- **Grade Management**:
  - Add, delete, and modify grades.
  - View grade reports.

- **Authentication**:
  - User registration and login with password encryption.

## Testing
To run the unit tests, use the following command:
python -m unittest test_checkmygrade.py

## File Structure 
CheckMyGrade/
├── app.py                  # Flask application

├── test_checkmygrade.py    # Unit tests -- python -m unittest test_checkmygrade.py

├── generate_students.py    # Script to generate student records

├── students.csv            # Student data

├── courses.csv             # Course data

├── professors.csv          # Professor data

├── grades.csv              # Grade data

├── login.csv               # User login data

├── README.md               # Project documentation

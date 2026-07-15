# CODSOFT_TASKSNO
CodSoft Backend Development Internship - Task 1: Student Record Management API built with Flask and MySQL
# CodSoft Task 1 - Student Record Management API

Backend REST API to manage students, courses, and enrollments — built as part of the CodSoft Backend Development Internship.

## Tech Stack
- Python (Flask)
- MySQL
- SQLAlchemy (ORM)
- Marshmallow (data validation)

## Features
- CRUD operations for Students, Courses, and Enrollments
- Data validation on all incoming requests
- Search, filter, sort, and pagination on student records
- Proper HTTP status codes and error handling

## API Endpoints

### Students
- `POST /students` - Create a student
- `GET /students` - Get all students (supports search, filter, sort, pagination)
- `GET /students/<id>` - Get a single student
- `PUT /students/<id>` - Update a student
- `DELETE /students/<id>` - Delete a student

### Courses
- `POST /courses` - Create a course
- `GET /courses` - Get all courses
- `PUT /courses/<id>` - Update a course
- `DELETE /courses/<id>` - Delete a course

### Enrollments
- `POST /enrollments` - Enroll a student in a course
- `GET /enrollments` - Get all enrollments
- `DELETE /enrollments/<id>` - Delete an enrollment

## How to Run
1. Install dependencies: `pip install flask flask-sqlalchemy flask-marshmallow marshmallow-sqlalchemy pymysql`
2. Create a MySQL database named `student_db`
3. Update database credentials in `config.py`
4. Run the server: `python app.py`

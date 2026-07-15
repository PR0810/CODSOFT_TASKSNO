from flask import Flask, request, jsonify
from config import Config
from models import db, Student, Course, Enrollment
from schemas import ma, student_schema, students_schema, course_schema, courses_schema, enrollment_schema, enrollments_schema
from marshmallow import ValidationError

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

# ---------- STUDENT APIs ----------

@app.route('/students', methods=['POST'])
def create_student():
    try:
        data = student_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    student = Student(name=data['name'], email=data['email'], age=data['age'])
    db.session.add(student)
    db.session.commit()
    return jsonify(student_schema.dump(student)), 201

@app.route('/students', methods=['GET'])
def get_students():
    query = Student.query

    # Search by name
    search = request.args.get('search')
    if search:
        query = query.filter(Student.name.ilike(f'%{search}%'))

    # Filter by age
    age = request.args.get('age')
    if age:
        query = query.filter(Student.age == int(age))

    # Sorting
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    column = getattr(Student, sort_by, Student.id)
    query = query.order_by(column.desc() if order == 'desc' else column.asc())

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "students": students_schema.dump(pagination.items)
    }), 200

@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student_schema.dump(student)), 200

@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    try:
        data = student_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        setattr(student, key, value)
    db.session.commit()
    return jsonify(student_schema.dump(student)), 200

@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted"}), 200


# ---------- COURSE APIs ----------

@app.route('/courses', methods=['POST'])
def create_course():
    try:
        data = course_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
    course = Course(name=data['name'], duration=data['duration'])
    db.session.add(course)
    db.session.commit()
    return jsonify(course_schema.dump(course)), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify(courses_schema.dump(courses)), 200

@app.route('/courses/<int:id>', methods=['PUT'])
def update_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    try:
        data = course_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400
    for key, value in data.items():
        setattr(course, key, value)
    db.session.commit()
    return jsonify(course_schema.dump(course)), 200

@app.route('/courses/<int:id>', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get(id)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": "Course deleted"}), 200


# ---------- ENROLLMENT APIs ----------

@app.route('/enrollments', methods=['POST'])
def create_enrollment():
    try:
        data = enrollment_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if not Student.query.get(data['student_id']):
        return jsonify({"error": "Student does not exist"}), 400
    if not Course.query.get(data['course_id']):
        return jsonify({"error": "Course does not exist"}), 400

    enrollment = Enrollment(student_id=data['student_id'], course_id=data['course_id'])
    db.session.add(enrollment)
    db.session.commit()
    return jsonify(enrollment_schema.dump(enrollment)), 201

@app.route('/enrollments', methods=['GET'])
def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify(enrollments_schema.dump(enrollments)), 200

@app.route('/enrollments/<int:id>', methods=['DELETE'])
def delete_enrollment(id):
    enrollment = Enrollment.query.get(id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found"}), 404
    db.session.delete(enrollment)
    db.session.commit()
    return jsonify({"message": "Enrollment deleted"}), 200


@app.route('/')
def home():
    return "Student Record API is running!"

if __name__ == '__main__':
    app.run(debug=True)
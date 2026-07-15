from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class StudentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    age = fields.Integer(required=True, validate=validate.Range(min=1, max=100))

class CourseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    duration = fields.String(required=True)

class EnrollmentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    student_id = fields.Integer(required=True)
    course_id = fields.Integer(required=True)

student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)
enrollment_schema = EnrollmentSchema()
enrollments_schema = EnrollmentSchema(many=True)
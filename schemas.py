
from flask_marshmallow import Marshmallow
from marshmallow import fields, validate

ma = Marshmallow()

class ContactSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    phone = fields.String(required=True, validate=validate.Length(min=10, max=15))
    address = fields.String()
    company = fields.String()

contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
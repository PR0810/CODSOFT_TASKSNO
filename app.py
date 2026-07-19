from flask import Flask, request, jsonify
from config import Config
from models import db, Contact
from schemas import ma, contact_schema, contacts_schema
from marshmallow import ValidationError

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/contacts', methods=['POST'])
def create_contact():
    try:
        data = contact_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if Contact.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Contact with this email already exists"}), 400
    if Contact.query.filter_by(phone=data['phone']).first():
        return jsonify({"error": "Contact with this phone number already exists"}), 400

    contact = Contact(**data)
    db.session.add(contact)
    db.session.commit()
    return jsonify(contact_schema.dump(contact)), 201

@app.route('/contacts', methods=['GET'])
def get_contacts():
    query = Contact.query

    search = request.args.get('search')
    if search:
        query = query.filter(
            (Contact.name.ilike(f'%{search}%')) |
            (Contact.email.ilike(f'%{search}%')) |
            (Contact.phone.ilike(f'%{search}%'))
        )

    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    column = getattr(Contact, sort_by, Contact.id)
    query = query.order_by(column.desc() if order == 'desc' else column.asc())

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        "total": pagination.total,
        "page": page,
        "per_page": per_page,
        "contacts": contacts_schema.dump(pagination.items)
    }), 200

@app.route('/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    return jsonify(contact_schema.dump(contact)), 200

@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"error": "Contact not found"}), 404

    try:
        data = contact_schema.load(request.json, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    for key, value in data.items():
        setattr(contact, key, value)
    db.session.commit()
    return jsonify(contact_schema.dump(contact)), 200

@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    db.session.delete(contact)
    db.session.commit()
    return jsonify({"message": "Contact deleted"}), 200

@app.route('/')
def home():
    return "Contact Management API is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5001)

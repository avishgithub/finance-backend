from flask import request, Blueprint
from models import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json

    if not data:
        return {"error": "Invalid JSON input"}, 400

    if not data.get('name') or not data.get('email') or not data.get('role'):
        return {"error": "Missing required fields"}, 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return {"error": "User already exists"}, 400

    user = User(
        name=data['name'],
        email=data['email'],
        role=data['role'],
        status='active'
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "User created successfully"}, 201


@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return [{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "role": u.role,
        "status": u.status
    } for u in users]
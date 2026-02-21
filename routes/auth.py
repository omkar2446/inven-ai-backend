from flask import Blueprint, request, jsonify
from models.user import User
from models import db
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ⭐ REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():

    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify(message="Missing fields"), 400

    # email exists
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify(message='Email already exists'), 400

    user = User(
        name=data.get('name'),
        email=data.get('email'),
        role=data.get('role','retailer')
    )

    user.set_password(data.get('password'))

    db.session.add(user)
    db.session.commit()

    return jsonify(message='User created'), 201


# ⭐ LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not user.check_password(data.get('password')):
        return jsonify(message='Invalid credentials'), 401

    # ⭐ send minimal identity (best practice)
    token_data = {
        "id": user.id,
        "email": user.email,
        "role": user.role
    }

    access_token = create_access_token(identity=token_data)

    return jsonify(access_token=access_token), 200
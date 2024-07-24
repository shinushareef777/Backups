from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from .models import User
from . import db
from .validations import UserRegister
from pydantic import ValidationError

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    try:
        user_data=UserRegister(**data)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    if user:
        return jsonify({"message": f"{user.username} already exists"}), 400

    new_user = User(username=data['username'], role=data['role'])

    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "new user created"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  user = User.query.filter_by(username=data['username']).first()
  if user and user.check_password(password=data['password']):
    access_token = create_access_token(identity={'username': user.username, 'role': user.role})
    refresh_token = create_refresh_token(identity={'username': user.username, 'role': user.role})
    return jsonify(access_token=access_token, refresh_token=refresh_token)
  return jsonify({"error":"invalid credentials"}), 401

@auth_bp.route('/refresh',  methods=['POST'])
@jwt_required(refresh=True)
def refresh():
  current_user = get_jwt_identity()
  new_access_token = create_access_token(identity=current_user)
  return jsonify(new_access_token)

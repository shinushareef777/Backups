from .auth import auth_bp
from .decorators import role_required
from .models import User
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required


user_bp = Blueprint('app', __name__)


@user_bp.route("/users", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_users():
    users = User.query.all()
    return jsonify([{"username": user.username, "role": user.role} for user in users])


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@jwt_required()
@role_required("admin")
def get_user(user_id):
  user = User.query.get_or_404(user_id)
  return jsonify({"username": user.username, "role": user.role})

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import User
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods = ["POST"])
def login():
    data = request.get_json()
    email = data.get("email", None)
    password = data.get("password", None)

    user = User.query.filter_by(email = email).first()

    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({"access token": access_token})
    else:
        return jsonify({"error":"Incorrect email/password."})
    
#check current user
@auth_bp.route("/current_user")
@jwt_required()
def current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    return jsonify({"username":user.username, "email": user.email, "phone_number": user.phone_number})



from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/add_user", methods = ["POST"])
def add_user():
    data = request.get_json()
    username = data["username"]
    email = data["email"]
    password = generate_password_hash(data["password"])
    phone_number = data["phone_number"]

    check_name = User.query.filter_by(username=username).first()
    check_email = User.query.filter_by(email=email).first()
    check_number = User.query.filter_by(phone_number=phone_number).first()

    if check_name or check_email or check_number:
        return jsonify({"error": "name, email or phone number already exists."})
    else:
        new_user = User(username=username, email=email, password=password, phone_number=phone_number)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "user added successfully"})
    
#fetch user
@user_bp.route("/user")
@jwt_required()
def fetch_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user:
        return jsonify({"username":user.username, "email": user.email, "phone_number": user.phone_number})
    else:
        return jsonify({"error": "user doesn't exist."})
    
#update user    
@user_bp.route("/update_user", methods=["PATCH"])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user:
        data = request.get_json()
        username = data.get("username", user.username)
        email = data.get("email", user.email)
        password = generate_password_hash(data.get("password", user.password))
        phone_number = data.get("phone_number", user.phone_number)

        check_name = User.query.filter_by(username=username and id!=user_id).first()
        check_email = User.query.filter_by(email=email and id!=user_id).first()
        check_number = User.query.filter_by(phone_number=phone_number and id!=user_id).first()

        if check_email or check_name or check_number:
            return jsonify({"error": "name, email or phone number already exists."})
        else:
            user.username = username
            user.email = email
            user.password = password
            user.phone_number = phone_number

            db.session.commit()
            return jsonify({"msg": "user updated successfully"})
    else:
        return jsonify({"error": "user doesn't exist."})


#delete user
@user_bp.route("/delete_user", methods=["DELETE"])
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "user deleted successfully."})
    else:
        return jsonify({"error": "user doesn't exist."})

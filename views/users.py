from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db
from app import app, mail
from flask_mail import Message

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/user/register", methods = ["POST"])
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
        try:
            msg = Message(
                subject="Welcome to Todo App",
                sender=app.config["MAIL_DEFAULT_SENDER"],
                recipients=[email],
                body="This is a test email sent from a Flask Application"

            )
            mail.send(msg)
            return jsonify({"success":"User saved successfully!"}), 201
        
        except Exception as e:
            return jsonify({"message": f"Failed to send {e}"})
    
#fetch user
@user_bp.route("/user")
@jwt_required()
def fetch_user():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email = user_email).first()

    if user:
        return jsonify({"username":user.username, "email": user.email, "phone_number": user.phone_number})
    else:
        return jsonify({"error": "user doesn't exist."})
    
#fetch user with orders
@user_bp.route("/user/orders")
@jwt_required()
def fetch_user_orders():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email = user_email).first()

    if user:
        orders = user.order
        if orders:
    
            orders_list = [
                {
                    "order_ref": order.order_ref,
                    "items_ordered": order.items_ordered,
                    "total_amount": order.total_amount,
                    "status": order.status,
                    "user_id": order.user_id,
                    "date_ordered": order.date_ordered,
                }
                for order in orders
            ]

            return jsonify({
                "username": user.username,
                "email": user.email,
                "phone_number": user.phone_number,
                "orders": orders_list
            }), 200
        else:
            return jsonify({"msg": "No orders found for this user."})

    else:
        return jsonify({"error": "user doesn't exist."})

    
#update user    
@user_bp.route("/user/update", methods=["PATCH"])
@jwt_required()
def update_user():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()

    if user:
        data = request.get_json()
        username = data.get("username", user.username)
        email = data.get("email", user.email)
        phone_number = data.get("phone_number", user.phone_number)

        check_name = User.query.filter_by(username=username and email!=user_email).first()
        check_email = User.query.filter_by(email=email and email!=user_email).first()
        check_number = User.query.filter_by(phone_number=phone_number and email!=user_email).first()

        if check_email or check_name or check_number:
            return jsonify({"error": "name, email or phone number already exists."})
        else:
            user.username = username
            user.email = email
            user.phone_number = phone_number

            db.session.commit()
            return jsonify({"msg": "user updated successfully"})
    else:
        return jsonify({"error": "user doesn't exist."})
    
#update user password    
@user_bp.route("/user/updatepassword", methods=["PATCH"])
@jwt_required()
def update_user_password():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()

    if user:
        data = request.get_json()
        password = generate_password_hash(data.get("password", user.password))

        if check_password_hash(user.password, password):
            return jsonify({"error":"password not changed"})
        else:
            user.password = password
            db.session.commit()
            return jsonify({"msg": "user updated successfully"})
    else:
        return jsonify({"error": "user doesn't exist."})


#delete user
@user_bp.route("/user/delete_account", methods=["DELETE"])
@jwt_required()
def delete_user():
    user_email = get_jwt_identity()
    user = User.query.filter_by(email=user_email).first()

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "user deleted successfully."})
    else:
        return jsonify({"error": "user doesn't exist."})
    


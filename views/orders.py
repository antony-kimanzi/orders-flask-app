from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, User, db
from datetime import datetime
import uuid

order_bp = Blueprint("order_bp", __name__)


# add order
@order_bp.route("/order/add", methods=["POST"])
@jwt_required()
def add_order():
    user_email = get_jwt_identity()
    
    data = request.get_json()

    check_user = User.query.filter_by(email=user_email).first()

    if check_user:
        order_ref = str(uuid.uuid4().hex[:6]).upper()
        items_ordered = data["items_ordered"]
        total_amount = data["total_amount"]
        status = data["status"]
        date_ordered = datetime.strptime(data["date_ordered"], "%Y-%m-%d %H:%M:%S")
        order_user_id = check_user.id
        new_order = Order(order_ref=order_ref, user_id=order_user_id, items_ordered=items_ordered, total_amount=total_amount, status=status, date_ordered=date_ordered)

        db.session.add(new_order)
        db.session.commit()
        return jsonify({"msg": "order added successfully"})
    else:
        return jsonify({"error": "user should login to place order"})
    
# Fetch all user's orders
@order_bp.route("/orders")
@jwt_required()
def fetch_order():
    user_email = get_jwt_identity()

    # Query for all orders by the user
    order_details = Order.query.filter_by(email=user_email).all()

    if order_details:  # Check if there are any orders
        if len(order_details) == 1:  # Single order case
            order = order_details[0]  # Extract the single order from the list
            return jsonify({
                "order_ref": order.order_ref,
                "items_ordered": order.items_ordered,
                "total_amount": order.total_amount,
                "status": order.status,
                "user_id": order.user_id,
                "date_ordered": order.date_ordered
            })
        else:  # Multiple orders case
            orders = [
                {
                    "order_ref": order.order_ref,
                    "items_ordered": order.items_ordered,
                    "total_amount": order.total_amount,
                    "status": order.status,
                    "user_id": order.user_id,
                    "date_ordered": order.date_ordered
                }
                for order in order_details
            ]
            return jsonify(orders)
    else:  
        return jsonify({"msg": "User hasn't ordered anything"}), 404

# Fetch a specific user's order
@order_bp.route("/order/<string:order_ref>")
@jwt_required()
def fetch_single_order(order_ref):
    user_email = get_jwt_identity()

    order = Order.query.filter_by(email=user_email, order_ref=order_ref).first()

    if order:
        return jsonify({
            "order_ref": order.order_ref,
            "items_ordered": order.items_ordered,
            "total_amount": order.total_amount,
            "status": order.status,
            "user_id": order.user_id,
            "date_ordered": order.date_ordered
        })
    else:  
        return jsonify({"msg": "The specific order doesn't exist"}), 404

    
#update order
@order_bp.route("/order/update/<string:order_ref>", methods=["PATCH"])
@jwt_required()
def update_order(order_ref):
    user_email = get_jwt_identity()

    data = request.get_json()

    order = Order.query.filter_by(email=user_email, order_ref=order_ref).first()

    if order:
        items_ordered = data.get("items_ordered", order.items_ordered)
        total_amount = data.get("total_amount", order.total_amount)
        status = data.get("status", order.status)

        order.items_ordered = items_ordered
        order.total_amount = total_amount
        order.status = status
        

        db.session.commit()
        return jsonify({"msg": "order updated successfully"})
    else:
        return jsonify({"msg": "Order not found or not authorized"})

#delete order
@order_bp.route("/order/delete/<string:order_ref>", methods=["DELETE"])
@jwt_required()
def delete_order(order_ref):
    user_email = get_jwt_identity()
    order = Order.query.filter_by(email = user_email, order_ref = order_ref).first()

    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({"msg":"order deleted successfully"})
    else:
        return jsonify({"msg":"order doesn't exist"})

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, User, db
from datetime import datetime

order_bp = Blueprint("order_bp", __name__)


# add order
@order_bp.route("/add_order", methods=["POST"])
@jwt_required()
def add_order():
    user_id = get_jwt_identity()
    
    data = request.get_json()
    items_ordered = data["items_ordered"]
    total_amount = data["total_amount"]
    status = data["status"]
    date_ordered = datetime.strptime(data["date_ordered"], "%Y-%m-%d %H:%M:%S")
    order_user_id = user_id

    check_user = User.query.filter_by(id=user_id).first()

    if check_user:
        new_order = Order(user_id=order_user_id, items_ordered=items_ordered, total_amount=total_amount, status=status, date_ordered=date_ordered)

        db.session.add(new_order)
        db.session.commit()
        return jsonify({"msg": "order added successfully"})
    else:
        return jsonify({"error": "user should login to place order"})
    
# Fetch order
@order_bp.route("/order")
@jwt_required()
def fetch_order():
    user_id = get_jwt_identity()

    # Query for all orders by the user
    order_details = Order.query.filter_by(user_id=user_id).all()

    if order_details:  # Check if there are any orders
        if len(order_details) == 1:  # Single order case
            order = order_details[0]  # Extract the single order from the list
            return jsonify({
                "items_ordered": order.items_ordered,
                "total_amount": order.total_amount,
                "status": order.status,
                "user_id": order.user_id,
                "date_ordered": order.date_ordered
            })
        else:  # Multiple orders case
            orders = [
                {
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
    
    #update order
            

    



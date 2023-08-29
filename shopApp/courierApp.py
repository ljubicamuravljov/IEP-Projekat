import csv
import io
import re

from flask import Flask, request, Response, jsonify
from datetime import datetime
# from authentication.models import User
from configuration import Configuration
from models import database, Product, ProductCategories, Category, Order, OrderProducts

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity, \
    create_refresh_token

from decorator import roleCheck

application = Flask(__name__)
application.config.from_object(Configuration)

jwt = JWTManager(application)


@application.route("/orders_to_deliver", methods=["GET"])
@roleCheck(role="courier")
def ordersToDeliver():
    orders = Order.query.filter(Order.status == "CREATED").all()

    ordersList = []
    for order in orders:
        ordersList.append({
            'id': order.id,
            'email': order.userEmail
        })

    return jsonify(orders=ordersList), 200


@application.route("/pick_up_order", methods=["POST"])
@roleCheck(role="courier")
def pickUpOrder():
    id = request.json.get("id", None)

    if id is None:
        return jsonify(message="Missing order id."), 400

    try:
        id = int(id)
    except ValueError:
        return jsonify(message="Invalid order id."), 400

    if id <= 0:
        return jsonify(message="Invalid order id."), 400

    order = Order.query.filter(Order.id == id).first()
    if order is None:
        return jsonify(message="Invalid order id."), 400

    if order.status != "CREATED":
        return jsonify(message="Invalid order id."), 400

    order.status = "PENDING"
    database.session.commit()
    return Response(200)


@application.route("/", methods=["GET"])
def index():
    return "Hello courier!"


if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5003)

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


@application.route("/search", methods=["GET"])
@roleCheck(role="customer")
def search():
    name=request.args.get("name","")
    catName=request.args.get("category","")

    categories=Category.query.join(ProductCategories).join(Product).filter(Product.name.like(f"%{name}%")).filter(Category.name.like(f"%{catName}%")).all()
    products=Product.query.join(ProductCategories).join(Category).filter(Product.name.like(f"%{name}%")).filter(Category.name.like(f"%{catName}%")).all()
    productRes=[]
    cateRes=[category.name for category in categories]
    for product in products:
        prodJson={
            "categories":[category.name for category in product.categories],
            "id":product.id,
            "name":product.name,
            "price":product.price
        }
        productRes.append(prodJson)


    return jsonify(categories=cateRes,products=productRes)

@application.route("/order",methods=["POST"])
@roleCheck(role="customer")
def order():
    req=request.json.get("requests",None)

    if req is None:
        return jsonify({"message": "Field requests is missing."}), 400

    ind = 0
    allRows=[]
    for row in req:
        id=row.get('id',None)
        quantity=row.get('quantity',None)


        if  id is None:
            return jsonify({"message": "Product id is missing for request number {}.".format(ind)}), 400


        if quantity is None:

            return jsonify({"message": "Product quantity is missing for request number {}.".format(ind)}), 400


        try :
            id=int(id)
        except ValueError:
            return jsonify({"message": "Invalid product id for request number {}.".format(ind)}), 400

        if id<=0:
            return jsonify({"message": "Invalid product id for request number {}.".format(ind)}), 400

        try :
            quantity=int(quantity)
        except ValueError:
            return jsonify({"message": "Invalid product quantity for request number {}.".format(ind)}), 400
        if quantity<=0:
            return jsonify({"message": "Invalid product quantity for request number {}.".format(ind)}), 400

        product=Product.query.filter(Product.id==id).first()
        if product is None:
            return jsonify({"message": "Invalid product for request number {}.".format(ind)}), 400


        allRows.append(row)
        ind+=1

    email = get_jwt_identity()
    # allProductsList=[]
    totalPrice=0
    newOrder = Order( timestamp=datetime.now(), userEmail=email)
    database.session.add(newOrder)
    database.session.commit()
    for row in allRows:
        curId=int(row.get('id',0))
        curQ=int(row.get('quantity',0))

        product=Product.query.filter(Product.id==curId).first()

        # tmpProd={
        #     'categories':[cat.name for cat in product.categories],
        #     'name':product.name,
        #     'price':product.price,
        #     'quantity':curQ
        # }
        totalPrice+=product.price*curQ

        # allProductsList.append(tmpProd)


        newProdOrder=OrderProducts(productId=curId, orderId=newOrder.id,quantity=curQ)
        database.session.add(newProdOrder)
        database.session.commit()


    newOrder.price=totalPrice
    database.session.commit()

    return jsonify(id=newOrder.id),200


@application.route("/status",methods=["GET"])
@roleCheck(role="customer")
def status():
    email = get_jwt_identity()

    usersOrders=Order.query.filter(Order.userEmail==email).all()


    ordersInfo=[]

    for order in usersOrders:

        products = Product.query.join(OrderProducts).join(Order).filter(Order.id==order.id).all()
        allProducts=[]
        for product in products:

            quantity=OrderProducts.query.filter(OrderProducts.productId==product.id).filter(OrderProducts.orderId==order.id).first().quantity
            tmpProd = {
              'categories':[cat.name for cat in product.categories],
              'name':product.name,
              'price':product.price,
              'quantity':quantity
            }
            allProducts.append(tmpProd)

        tmpOrder={
            'products':allProducts,
            'price':order.price,
            'status':order.status,
            'timestamp':order.timestamp.isoformat()
        }
        ordersInfo.append(tmpOrder)

    return jsonify(orders=ordersInfo),200


@application.route("/", methods=["GET"])
def index():
    return "Hello customer!"





if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5001)
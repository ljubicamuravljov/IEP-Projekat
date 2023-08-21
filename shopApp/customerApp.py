import csv
import io
import re

from flask import Flask, request, Response, jsonify
from configuration import Configuration
from models import database, Product, ProductCategories, Category

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

@application.route("/", methods=["GET"])
def index():
    return "Hello customer!"





if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5001)
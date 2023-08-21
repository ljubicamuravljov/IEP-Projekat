import csv
import io
import re

from flask import Flask,request,Response,jsonify
from configuration import Configuration
from models import database,Product,ProductCategories,Category

from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt,get_jwt_identity,create_refresh_token


from decorator import roleCheck

application = Flask(__name__)
application.config.from_object(Configuration)





jwt=JWTManager(application)


@application.route("/update",methods=["POST"])
@roleCheck(role="owner")
def update():


    if "file" not in request.files:
        return jsonify({"message": "Field file is missing."}), 400

    content=request.files["file"].stream.read().decode("utf-8")
    stream=io.StringIO(content)
    reader=csv.reader(stream)

    ind=0
    rows=[]
    productNames=[]
    for row in reader:
        print("----------------------------")
        print(str(row))

        if len(row)!=3:
            return jsonify({"message": "Incorrect number of values on line {}.".format(ind)}), 400


        try:
            float(row[2])
        except ValueError:
            return jsonify({"message": "Incorrect price on line {}.".format(ind)}), 400
            
        if float(row[2]) <= 0:
            return jsonify({"message": "Incorrect price on line {}.".format(ind)}), 400

        #znaci, treba mi,ukoliko ovaj name vec postoji-> ne moze, ili ukoliko se dva put pojavljuje name u fajlu?
        name=row[1]
        prodTmp=Product.query.filter(Product.name == name).first()
        if prodTmp is not None  or  name in productNames:
            return jsonify({"message": "Product {} already exists.".format(name)}), 400
        rows.append(row)
        productNames.append(name)

        ind = ind+1


    for row in rows:
        print(str(row))
        newProd=Product(name=row[1],price=float(row[2]))
        database.session.add(newProd)
        database.session.commit()
        for cat in row[0].split("|"):
            category=Category.query.filter(Category.name==cat).first()
            if category is None:
                category=Category(name=cat)
                database.session.add(category)
                database.session.commit()

            productCat=ProductCategories(productId=newProd.id,categoryId=category.id)
            database.session.add(productCat)
            database.session.commit()



    return Response(200)

@application.route("/", methods=["GET"])
def index():
    return "Hello owner!"

@application.route("/products", methods=["GET"])
def products():
    return str(Product.query.all())

@application.route("/categories", methods=["GET"])
def categories():
    return str(Category.query.all())

@application.route("/prodcat", methods=["GET"])
def prodcat():
    return str(ProductCategories.query.all())

@application.route("/delprod", methods=["POST"])
def delprod():
    name=request.json.get("name", "")
    product=Product.query.filter(Product.name==name).first()
    database.session.delete(product)
    database.session.commit()
    return str(Product.query.all())

@application.route("/delcat", methods=["POST"])
def delcat():
    name=request.json.get("name", "")
    category=Category.query.filter(Category.name==name).first()
    database.session.delete(category)
    database.session.commit()
    return str(Category.query.all())

@application.route("/delete", methods=["POST"])
def delete():
    categories=Category.query.all()
    for category in categories:
        database.session.delete(category)
        database.session.commit()

    products=Product.query.all()
    for product in products:
        database.session.delete(product)
        database.session.commit()
    return str(Category.query.all())

@application.route("/delprodcat", methods=["POST"])
def delprodcat():
    id=request.json.get("id", "")
    productcat=ProductCategories.query.filter(ProductCategories.id==id).first()
    database.session.delete(productcat)
    database.session.commit()
    return str(ProductCategories.query.all())

if(__name__=="__main__"):
    database.init_app(application)
    application.run(debug=True,host="0.0.0.0",port=5000)
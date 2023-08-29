import re

from flask import Flask, request, Response, jsonify
from configuration import Configuration
from models import database, User
from email.utils import parseaddr
from redis import Redis
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity, \
    create_refresh_token
from sqlalchemy import and_

application = Flask(__name__)
# application.config[""]
application.config.from_object(Configuration)

regEmail = r"^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$"


@application.route("/register_customer", methods=["POST"])
def registerCustomer():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0
    forenameEmpty = len(forename) == 0
    surnameEmpty = len(surname) == 0

    if forenameEmpty:
        return jsonify(message="Field forename is missing."), 400
    elif surnameEmpty:
        return jsonify(message="Field surname is missing."), 400
    elif emailEmpty:
        return jsonify(message="Field email is missing."), 400
    elif passwordEmpty:
        return jsonify(message="Field password is missing."), 400
    elif not re.match(regEmail, email) or len(email) > 256:
        return jsonify(message="Invalid email."), 400
    elif len(password) < 8 or len(password) > 256:
        return jsonify(message="Invalid password."), 400

    checkUser = User.query.filter(User.email == email).first()
    if checkUser != None:
        return jsonify(message="Email already exists."), 400

    database.session.add(User(forename=forename, surname=surname, email=email, password=password, role="customer"))
    database.session.commit()

    return Response(status=200)


@application.route("/register_courier", methods=["POST"])
def registerCourier():
    email = request.json.get("email", "")
    password = request.json.get("password", "")
    forename = request.json.get("forename", "")
    surname = request.json.get("surname", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0
    forenameEmpty = len(forename) == 0
    surnameEmpty = len(surname) == 0
    if forenameEmpty:
        return jsonify(message="Field forename is missing."), 400
    elif surnameEmpty:
        return jsonify(message="Field surname is missing."), 400
    elif emailEmpty:
        return jsonify(message="Field email is missing."), 400
    elif passwordEmpty:
        return jsonify(message="Field password is missing."), 400



    elif not re.match(regEmail, email) or len(email) > 256:
        return jsonify(message="Invalid email."), 400
    elif len(password) < 8 or len(password) > 256:
        return jsonify(message="Invalid password."), 400

    checkUser = User.query.filter(User.email == email).first()
    if checkUser is not None:
        return jsonify(message="Email already exists."), 400

    database.session.add(User(forename=forename, surname=surname, email=email, password=password, role="courier"))
    database.session.commit()

    return Response(status=200)


jwt = JWTManager(application)


@application.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", "")
    password = request.json.get("password", "")

    emailEmpty = len(email) == 0
    passwordEmpty = len(password) == 0

    if emailEmpty:
        return jsonify(message="Field email is missing."), 400
    elif passwordEmpty:
        return jsonify(message="Field password is missing."), 400
    elif not re.match(regEmail, email) or len(email) > 256:
        return jsonify(message="Invalid email."), 400
    # elif len(password) < 8 or len(password) > 256:
    #     return jsonify({"message": "Invalid password"}), 400

    user = User.query.filter(and_(User.email == email, User.password == password)).first()

    if not user:
        return jsonify(message="Invalid credentials."), 400

    additionalClaims = {
        "forename": user.forename,
        "surname": user.surname,
        "roles": user.role
    }

    accessToken = create_access_token(identity=user.email, additional_claims=additionalClaims)

    # return Response(accesToken,status=200)
    return jsonify(accessToken=accessToken)


@application.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    email = get_jwt_identity()
    user = User.query.filter(User.email == email).first()
    if user is None:
        return jsonify(message="Unknown user."), 400
    database.session.delete(user)
    database.session.commit()

    return Response(status=200)


@application.route("/", methods=["GET"])
def index():
    return "Hello world!AA"


if (__name__ == "__main__"):
    database.init_app(application)
    application.run(debug=True, host="0.0.0.0", port=5002)

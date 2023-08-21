
from functools import wraps

from flask import Response, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, jwt_required


def roleCheck(role):
    def innerRole(function):
        @jwt_required()
        @wraps(function)
        def decorater(*arguments,**keywordArguments):
            # verify_jwt_in_request()
            claims=get_jwt()

            if ("roles" in claims) and (role == claims["roles"]):
                return function(*arguments,**keywordArguments)
            else:
                return jsonify({"msg":"Missing Authorization Header"}),401

        return decorater
    return innerRole
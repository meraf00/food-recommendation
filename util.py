from functools import wraps
from flask import request, jsonify
import jwt
import os


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing"}), 400

        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            username = payload["username"]
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token is invalid"}), 400

        return f(*args, username=username, **kwargs)

    return decorated_function

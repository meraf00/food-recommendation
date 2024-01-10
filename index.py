from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import pymongo
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from util import login_required

load_dotenv()

app = Flask(__name__)

mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = mongo_client[os.getenv("MONGO_DB_NAME")]


def generate_token(user: dict):
    token = jwt.encode(
        {
            "username": user["username"],
            "exp": datetime.utcnow() + timedelta(days=1),
        },
        os.getenv("SECRET_KEY"),
        algorithm="HS256",
    )
    return token


@app.route("/api/auth/login", methods=["POST"])
def login():
    req = request.get_json()

    username = req.get("username")
    password = req.get("password")

    if not username or not password:
        return jsonify({"message": "Username or password is missing"}), 400

    user = db.users.find_one({"username": username})

    if not user:
        return jsonify({"message": "Invalid username or password"}), 404

    if check_password_hash(user.password, password):
        return jsonify({"token": generate_token()}), 200


@app.route("/api/auth/register", methods=["POST"])
def register():
    req = request.get_json()

    username = req.get("username")
    password = req.get("password")

    if not username or not password:
        return jsonify({"message": "Username or password is missing"}), 400

    user = db.users.find_one({"username": username})

    if user:
        return jsonify({"message": "Username already exists"}), 400

    db.users.insert_one(
        {
            "username": username,
            "password": generate_password_hash(password),
        }
    )

    return jsonify({"message": "User successfully registered"}), 201


@app.route("/api/user", methods=["DELETE"])
@login_required
def delete_profile(username: str):
    db.user.delete_one({username: username})

    return jsonify({"message": "User successfully deleted"}), 200


@app.route("/api/user/profile", methods=["POST"])
@login_required
def update_profile(username: str):
    req = request.get_json()

    if "username" in req or "password" in req or "_id" in req:
        return jsonify({"message": "Invalid request"}), 400

    db.user.update_one({username: username}, req, upsert=True)

    user = db.user.find_one({username: username})
    user.pop("password")

    return jsonify({"user": user}), 200


@app.route("/api/user/profile", methods=["GET"])
@login_required
def get_profile(username: str):
    user = db.user.find_one({username: username})
    user.pop("password")

    return jsonify({"user": user}), 200


@app.route("/api/user/food", methods=["GET"])
@login_required
def get_food_recommendation(username: str):
    ...


@app.route("/api/food", methods=["GET"])
@login_required
def get_food_by_ingredient(username: str):
    ...


@app.route("/api/food", methods=["POST"])
@login_required
def add_food(username: str):
    ...    
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
import pymongo
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from bson import json_util
import json

from util import login_required
import recommendation
from recommendation import recipe_tokenizer

load_dotenv()

app = Flask(__name__)

mongo_client = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = mongo_client[os.getenv("MONGO_DB_NAME")]


def parse_json(data):
    return json.loads(json_util.dumps(data))


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

    user = db.user.find_one({"username": username})

    if not user:
        return jsonify({"message": "Invalid username or password"}), 404

    if check_password_hash(user["password"], password):
        return jsonify({"token": generate_token(user)}), 200


@app.route("/api/auth/register", methods=["POST"])
def register():
    req = request.get_json()

    username = req.get("username")
    password = req.get("password")

    if not username or not password:
        return jsonify({"message": "Username or password is missing"}), 400

    user = db.user.find_one({"username": username})

    if user:
        return jsonify({"message": "Username already exists"}), 400

    db.user.insert_one(
        {
            "username": username,
            "password": generate_password_hash(password),
        }
    )

    return jsonify({"message": "User successfully registered"}), 201


@app.route("/api/user", methods=["DELETE"])
@login_required
def delete_profile(username: str):
    db.user.delete_one({"username": username})

    return jsonify({"message": "User successfully deleted"}), 200


@app.route("/api/user/profile", methods=["POST"])
@login_required
def update_profile(username: str):
    """
    Sample request body:
    {
        "weight": 52,
        "height": 175,
        "bmi": 16.9795918367
    }

    Sample response:
    {
        "user": {
            "_id": {
                "$oid": "65a05073b6729027356222be"
            },
            "bmi": 16.9795918367,
            "height": 175,
            "username": "test",
            "weight": 52
        }
    }
    """
    req = request.get_json()

    print(username)

    if "username" in req or "password" in req or "_id" in req:
        return jsonify({"message": "Invalid request"}), 400

    db.user.update_one({"username": username}, {"$set": req}, upsert=True)

    user = db.user.find_one({"username": username})
    user.pop("password")

    return jsonify({"user": parse_json(user)}), 200


@app.route("/api/user/profile", methods=["GET"])
@login_required
def get_profile(username: str):
    """
    Get profile of logged in user

    Sample response:
    {
        "user": {
            "_id": {
                "$oid": "65a05073b6729027356222be"
            },
            "bmi": 16.9795918367,
            "height": 175,
            "username": "test",
            "weight": 52
        }
    }
    """
    user = db.user.find_one({"username": username})
    user.pop("password")

    return jsonify({"user": parse_json(user)}), 200


@app.route("/api/user/food", methods=["GET"])
@login_required
def get_food_recommendation(username: str):
    """
    Get food recommendations for loggedin user

    Sample response:
    {
        "foods": [
            {
                "description": "Bread, white, commercially prepared, toasted",
                "category": "Cerials and Bakery Products",
                "nutrition": {
                    "energy_kcal": 253.1,
                    "protein_gm": 253.1,
                    "carbohydrate_gm": 253.1,
                    "total_sugar_gm": 253.1,
                    "dietary_fiber_gm": 253.1,
                    "total_fat_gm": 253.1,
                    "total_saturated_fatty_acids_gm": 253.1,
                    "total_monounsaturated_fatty_acids_gm": 253.1,
                    "total_polyunsaturated_fatty_acids_gm": 253.1,
                    "cholesterol_mg": 253.1,
                    "vitamin_e_mg": 253.1,
                    "calcium_mg": 253.1,
                    "phosphorus_mg": 253.1,
                    "magnesium_mg": 253.1,
                    "iron_mg": 253.1,
                    "zinc_mg": 253.1,
                    "copper_mg": 253.1,
                    "sodium_mcg": 253.1,
                    "potassium_mg": 253.1,
                    "selenium_mcg": 253.1,
                    "caffeine_mg": 253.1,
                }

            }
        ]
    }
    """

    user = db.user.find_one({"username": username})

    mean_user_attributes = {
        "weight": 76.410956,
        "height": 163.512096,
        "bmi": 28.100621,
        "upper_leg_length": 38.745666,
        "upper_arm_length": 36.566440,
        "arm_circumference": 31.807006,
        "waist_circumference": 94.448656,
        "hip_circumference": 105.696877,
        "systolic": 119.806263,
        "diastolic": 71.599455,
        "pulse": 71.893791,
    }

    user_vector = []

    for attr in mean_user_attributes:
        if attr not in user:
            user_vector.append(mean_user_attributes[attr])

        else:
            user_vector.append(user[attr])

    recommendations = recommendation.collab_filter(user_vector)

    foods = [{"nutrition": {}} for _ in range(len(recommendations))]

    for attrib, values in recommendations.items():
        for i, value in enumerate(values):
            if attrib == "Main food description":
                foods[i]["description"] = value

            elif attrib == "WWEIA Category description":
                foods[i]["category"] = value

            else:
                foods[i]["nutrition"][attrib] = value

    return jsonify({"foods": foods}), 200


@app.route("/api/food", methods=["GET"])
@login_required
def get_food_by_ingredient(username: str):
    """
    Sample request:

    GET /api/food?query=bread+milk

    Sample response:

    {
        "foods": [
            {
                "description": "Bread, white, commercially prepared, toasted",
                "category": "Cerials and Bakery Products",
                "nutrition": {
                    "energy_kcal": 253.1,
                    "protein_gm": 253.1,
                    "carbohydrate_gm": 253.1,
                    "total_sugar_gm": 253.1,
                    "dietary_fiber_gm": 253.1,
                    "total_fat_gm": 253.1,
                    "total_saturated_fatty_acids_gm": 253.1,
                    "total_monounsaturated_fatty_acids_gm": 253.1,
                    "total_polyunsaturated_fatty_acids_gm": 253.1,
                    "cholesterol_mg": 253.1,
                    "vitamin_e_mg": 253.1,
                    "calcium_mg": 253.1,
                    "phosphorus_mg": 253.1,
                    "magnesium_mg": 253.1,
                    "iron_mg": 253.1,
                    "zinc_mg": 253.1,
                    "copper_mg": 253.1,
                    "sodium_mcg": 253.1,
                    "potassium_mg": 253.1,
                    "selenium_mcg": 253.1,
                    "caffeine_mg": 253.1,
                }

            }
        ]
    }
    """

    query = request.args.get("query")

    recommendations = recommendation.find_similar_recipes(query)

    foods = [{"nutrition": {}} for _ in range(len(recommendations))]

    for attrib, values in recommendations.items():
        for i, value in enumerate(values):
            if attrib == "Main food description":
                foods[i]["description"] = value

            elif attrib == "WWEIA Category description":
                foods[i]["category"] = value

            else:
                foods[i]["nutrition"][attrib] = value

    return jsonify({"foods": foods}), 200


if __name__ == "__main__":
    app.run(debug=True)

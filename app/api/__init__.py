import os
from flask import Flask, jsonify
import redis
from dotenv import load_dotenv

load = load_dotenv()

db = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    return app

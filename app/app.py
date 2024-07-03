from flask import Flask, render_template, redirect, url_for, jsonify
from app.routers import orders
from app.utils.drone import Drone
from flask_cors import CORS
import os


app = Flask(__name__)

# Enable CORS
CORS(app) 

# Register the orders blueprint
app.register_blueprint(orders.bp)


@app.route("/")
def index():
    # simulate_drone()
    
    # Serve map
    return render_template("index.html")


def simulate_drone():
    Drone()


if __name__ == '__main__':
    app.run(debug=True, threaded=True)

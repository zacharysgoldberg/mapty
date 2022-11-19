from flask import Flask, redirect, url_for
from routers import order
import os

app = Flask(__name__)


app.register_blueprint(order.bp)


@app.route('/')
def index():
    return redirect(url_for('orders.orders'))


if __name__ == "__main__":
    port = os.getenv('PORT', 5000)
    host = os.getenv('HOST', '127.0.0.1')
    app.run(debug=True, threaded=True, host=host, port=port)

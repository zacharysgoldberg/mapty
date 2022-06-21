from api import create_app
from flask import render_template
from api import load
import os

app = create_app()


@app.route('/')
def index():
    return render_template('index.html')
    # return render_template('home.html')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(threaded=True, host='0.0.0.0', port=port, debug=True)

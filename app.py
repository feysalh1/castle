import os
import logging
from flask import Flask, render_template

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "baby_girl_app_secret")

@app.route('/')
def index():
    """Render the homepage of the Baby Girl app."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

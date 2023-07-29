"""
Main module of the server file
"""
# 3rd party moudles
from flask import render_template

# Local modules
import config


# Get the application instance
connex_app = config.connex_app


# Create a URL route in our application for "/"
@connex_app.route("/")
def home():
    """
    This function just responds to the browser URL
    localhost:5000/
    """
    return render_template("home.html")


if __name__ == "__main__":
    connex_app.run(debug=True)
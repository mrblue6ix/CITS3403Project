# the routes are the different URLs that the application implements.
from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    return render_template('home.html')

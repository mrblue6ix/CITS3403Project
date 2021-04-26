# the routes are the different URLs that the application implements.
from flask import render_template
from app import app

@app.route("/")
@app.route("/index")
def index():
    #change username to dynamically update for different users
    user = {'username': 'Jordan'}
    return render_template('home.html', user=user)

@app.route("/problem")
def problem():
    #change problem number/name to dynamically update
    problem = {'number': '1'}
    return render_template('problem.html', problem=problem)

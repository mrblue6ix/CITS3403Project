# the routes are the different URLs that the application implements.
from flask import render_template, flash, redirect
from flask_login import current_user, login_user
from flask import url_for
from app import app
from .forms import LoginForm, RegistrationForm

@app.route("/")
@app.route("/index")
def index():
    #change username to dynamically update for different users
    user = {'username': 'Jordan'}
    return render_template('home.html', user=user)

@app.route("/problem")
def problem():
    #change problem number/name to dynamically update
    #problem is variable to be passed into render_template
    problem = {'number': '1'}
    return render_template('problem.html', problem=problem)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    #if the form is correctly validated, flash a string then reidrect to homepage and log in
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        #Below, redirects to homepage (or other page) after user is logged in
        return redirect('/index')
    #if form couldn't be validated then render template for home.html so user can sign in again
    #maybe add a login.html where all logins happen???
    return render_template('home.html', title='Sign In', form=form)

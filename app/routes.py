# the routes are the different URLs that the application implements.
from flask import render_template, flash, redirect
from flask_login import current_user, login_user, logout_user
from flask import url_for
from app import app
from app.models import User
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

# logout the user
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # if we are in POST mode, check whether the user exists
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first()
        # if the user doesn't exist, flash back to the login screen.
        if u is None or not u.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            login_user(u, remember=form.remember_me.data)
            flash('You have logged in successfully!')
            return redirect(url_for('index'))
        #Below, redirects to homepage (or other page) after user is logged in
        return redirect('/index')
    #if form couldn't be validated then render template for home.html so user can sign in again
    #maybe add a login.html where all logins happen???
    return render_template('login.html', title='Sign In', form=form)

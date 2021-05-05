# the routes are the different URLs that the application implements.
from flask import render_template, flash, redirect
from flask_login import current_user, login_user, logout_user
from flask import url_for
from app import app, db
from app.models import User, Module, Activity
from .forms import LoginForm, RegistrationForm

@app.context_processor
def inject_navbar():
    modules = Module.query.order_by(Module.name).all()
    activities = Activity.query.all()
    return dict(modules=modules, activities=activities)

@app.route("/")
@app.route("/index")
def index():
    #change username to dynamically update for different users
    return render_template('home.html')

@app.route("/profile")
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template('profile.html', user=current_user)

@app.route("/learn/<module_name>/<activity_name>")
def problem(module_name, activity_name):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # Does the user have permission to access this activity?
    activity = Activity.query.filter_by(name=activity_name).first()
    module = Module.query.filter_by(name=module_name).first()
    if not activity or (activity not in module.activities):
        # The activity does not exist
        return render_template('errors/404.html')
    if not current_user.has_access(activity):
        dependencies = [(a.parentActivity.module, a.parentActivity) for a in activity.dependencies]
        return render_template('activity.html', locked=True, dependencies=dependencies)
    print(current_user.has_access(activity))
    return render_template('activity.html', activity=activity, module=module)

# logout the user
@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out successfully.')
    return redirect(url_for('index'))

@app.route('/tos')
def tos():
    return render_template('tos.html')

# register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # add user here if doesn't exist already
        user = User(username=form.username.data, email=form.email.data,
                    firstname=form.firstname.data, lastname=form.lastname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully registered.')

        # Generate UserActivities for modules that have no requirements
        first_module = Module.query.filter_by(dependencies=None).first()
        first_module.makeUserActivities(user)

        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)

# Route to login a user
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

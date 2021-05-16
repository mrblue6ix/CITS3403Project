# the routes are the different URLs that the application implements.
from flask import render_template, flash, redirect, request
from flask_login import current_user, login_user, logout_user
from flask import url_for
from app import app, db
from app.models import User, Module, Activity, UserActivity
from .forms import LoginForm, RegistrationForm
from functools import wraps
from difflib import SequenceMatcher
from sqlalchemy.sql import func
import time

# https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

@app.context_processor
def inject_navbar():
    modules = Module.query.order_by(Module.name).all()
    activities = Activity.query.all()
    return dict(modules=modules, activities=activities)

@app.route("/")
@app.route("/index")
def index():
    #change username to dynamically update for different users
    if current_user.is_authenticated:
        if current_user.is_admin:
            stats = []
            stats.append(('Total site users', User.query.count()))
            stats.append(('Number of activities', Activity.query.count()))
            stats.append(('Number of modules', Module.query.count()))
            return render_template('home.html', stats=stats)
        else:
            progress = UserActivity.query.filter_by(user_id=current_user.id, is_completed=1).count()/Activity.query.count() * 100
            return render_template('home.html', progress=f'{progress:.1f}')
    return render_template('home.html')

@app.route("/reset/<module_name>/<activity_name>")
def reset(module_name, activity_name):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    activity = Activity.query.filter_by(name=activity_name).first()
    module = Module.query.filter_by(name=module_name).first()
    if not activity or not module or (activity not in module.activities):
        # The activity or module does not exist
        return render_template("errors/500.html")
    current_user_activity = current_user.get_activity(activity)
    if not current_user_activity:
        return render_template("errors/403.html")
    return activity.prefill;  

@app.route('/stats/<module_name>/<activity_name>')
def stats(module_name, activity_name):
    if not current_user.is_authenticated or not current_user.is_admin:
        return redirect(url_for("index"))
    activity = Activity.query.filter_by(name=activity_name).first()
    module = Module.query.filter_by(name=module_name).first()
    stats = []
    stats.append(("Times this activity has been submitted", activity.times_submitted))
    stats.append(("Times this activity has been answered correctly", activity.times_right))
    if activity.times_submitted == 0:
        p_right = 0
    else:
        p_right = activity.times_right/activity.times_submitted * 100
    stats.append(("% correct", p_right))
    num_unique = User.query.filter(User.user_activities.any(activity_id=activity.id)).count()
    stats.append(("Unique users tried this activity",num_unique))

    return render_template('admin_activity.html', stats=stats, activity=activity)

@app.route("/test/<module_name>/<start>")
@app.route("/test/<module_name>")
def test(module_name, start=None):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    # Does the user have permission to access this activity?
    module = Module.query.filter_by(name=module_name).first()
    # A test should only have one activity
    activity = Activity.query.filter_by(module=module).first()
    if not activity or (activity not in module.activities):
        # The activity does not exist
        return render_template('errors/404.html')
    if current_user.is_admin:
        return redirect(url_for('stats', module_name=module_name, activity_name=activity.name))
    current_user_activity = current_user.get_activity(activity)
    if not current_user_activity:
        dependencies = [(a.parentActivity.module, a.parentActivity) for a in activity.dependencies]
        return render_template('activity.html', locked=True, dependencies=dependencies)
    if start:
        return render_template('start_test.html', module=module, activity=activity) 
    saved_code = current_user_activity.saved

    # If we haven't started the timer, start it now
    time_stop = current_user_activity.time_stop
    if time_stop == None:
        current_user_activity.set_timestop(activity.time_limit + time.time())
        time_stop = activity.time_limit + time.time()
        db.session.commit()
    elif time.time() > time_stop:
        current_user_activity.set_completion(1)
        return render_template('activity.html', saved=saved_code, activity=activity,
                                module=module, is_completed=1)

    return render_template('activity.html', saved=saved_code, time_stop=time_stop,
            activity=activity, module=module, is_completed=current_user_activity.is_completed)

@app.route("/save/<module_name>/<activity_name>", methods=["POST"])
def save(module_name, activity_name):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    activity = Activity.query.filter_by(name=activity_name).first()
    module = Module.query.filter_by(name=module_name).first()
    if not activity or not module or (activity not in module.activities):
        # The activity or module does not exist
        return render_template("errors/500.html")
    current_user_activity = current_user.get_activity(activity)
    if not current_user_activity:
        return render_template("errors/403.html")
    data = request.form['code']
    current_user_activity.save_code(data)
    db.session.commit()
    return {'saved':True}

# Receive an AJAX request from the browser
@app.route("/submit/<module_name>/<activity_name>", methods=["POST"])
def check_answer(module_name, activity_name):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    activity = Activity.query.filter_by(name=activity_name).first()
    module = Module.query.filter_by(name=module_name).first()
    if not activity or not module or (activity not in module.activities):
        # The activity or module does not exist
        return render_template("errors/500.html")
    current_user_activity = current_user.get_activity(activity)
    if not current_user_activity:
        return render_template("errors/403.html")

    if current_user_activity.is_completed:
        return {'message': "You have already completed this activity."}

    # check answer to the activity
    user_answer = request.form['answer'].strip()
    code = request.form['code'].strip()
    answer = str(activity.answer).strip()
    current_user.submit_one()
    activity.submit()
    if similar(user_answer, answer) > 0.95:
        activity.correct()
        # Answer is correct, unlock all activities that depend on this one.
        current_user_activity.set_completion(1)
        current_user.add_loc(len(code.split("\n")))
        unlocked = []
        for dependency in activity.parent_of:
            child = dependency.childActivity
            newActivity = child.makeUserActivity(current_user)
            # if it is a test, don't append the activity name
            if 'test' in child.module.name:
                unlocked.append((child.title, child.module.name))
            else:
                unlocked.append((child.title, child.module.name+"/"+child.name))
        db.session.commit()
        return {"message":activity.solution, "unlocked":sorted(unlocked, key=lambda x: x[1])}
    else:
        db.session.commit()
        return {'message': 'Wrong answer. Try again!'}

@app.route("/profile")
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template('profile.html', user=current_user)

@app.route("/learn/<module_name>/<activity_name>")
def learn(module_name, activity_name):
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    if current_user.is_admin:
        return redirect(url_for('stats', module_name=module_name, activity_name=activity_name))
    # Does the user have permission to access this activity?
    activity = Activity.query.filter_by(name=activity_name).first()
    module = Module.query.filter_by(name=module_name).first()
    if not activity or (activity not in module.activities):
        # The activity does not exist
        return render_template('errors/404.html')
    current_user_activity = current_user.get_activity(activity)
    if not current_user_activity:
        dependencies = [(a.parentActivity.module, a.parentActivity) for a in activity.dependencies]
        return render_template('activity.html', locked=True, dependencies=dependencies)

    saved_code = current_user_activity.saved
    print(saved_code)
    return render_template('activity.html', saved=saved_code, activity=activity,
                    module=module, is_completed=current_user_activity.is_completed)

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

        # Generate UserActivities for Activities that have no requirements
        activities = Activity.query.filter_by(dependencies=None).all()
        for activity in activities: 
            activity.makeUserActivity(user)
        db.session.commit()

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

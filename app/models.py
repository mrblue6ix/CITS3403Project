from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), index=True, unique=False)
    lastname = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    total_submissions = db.Column(db.Integer)
    lines_of_code = db.Column(db.Integer)
    num_correct = db.Column(db.Integer)
    num_incorrect = db.Column(db.Integer)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = 
    answer = 
    solution = 
    question = 

class Module(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = 
    description = 

class UserActivity(db.Model):
    user_activity_id = db.Column(db.Integer, primary_key=True)
    user_id = activity_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    count_submitted = db.Column(db.Integer)
    is_completed = db.Column(db.Integer)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = 
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class ActivityDependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer) #integer id of the parent activity
    child = db.Column(db.Integer)

class ModuleDependency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer) #integer id of the parent module
    child = db.Column(db.Integer)
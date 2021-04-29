import base64
from datetime import datetime, timedelta
from app import db
#from flask_login import UserMixin #idk what this is tbh
from werkzeug.security import generate_password_hash, check_password_hash
from flask import url_for
import os

#allows login to get User from db given the id
def load_student(id):
    return User.query.get(int(id))

class User(db.Model):
    __tablename__='users'
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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #can add more methods here
    #eg. for the example website from lectures, getProject(), getPartners() etc

class Activity(db.Model):
    __tablename__='activity'
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Integer) #added some dummy integer columns to test stuff first
    answer = db.Column(db.Integer)
    solution = db.Column(db.Integer)
    question = db.Column(db.Integer)

class Module(db.Model):
    __tablename__='module'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Integer)
    description = db.Column(db.Integer)

class UserActivity(db.Model):
    __tablename__='userActivity'
    user_activity_id = db.Column(db.Integer, primary_key=True)
    user_id = activity_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    count_submitted = db.Column(db.Integer)
    is_completed = db.Column(db.Integer)

class Submission(db.Model):
    __tablename__='Submission'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class ActivityDependency(db.Model):
    __tablename__='activityDependency'
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer) #integer id of the parent activity
    child = db.Column(db.Integer)

class ModuleDependency(db.Model):
    __tablename__='moduleDependency'
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer) #integer id of the parent module
    child = db.Column(db.Integer)
from datetime import datetime, timedelta
# Flask provides a mixin class that includes generic implementations for most
# user model classes.
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash
from app import login, db

#allows login to get User from db given the id
@login.user_loader
def load_student(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text, unique=False, nullable=False)
    lastname = db.Column(db.Text, unique=False, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    total_submissions = db.Column(db.Integer, default=0)
    lines_of_code = db.Column(db.Integer, default=0)
    num_correct = db.Column(db.Integer, default=0)
    num_incorrect = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    #can add more methods here
    #eg. for the example website from lectures, getProject(), getPartners() etc

class Activity(db.Model):
    __tablename__='activity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    title = db.Column(db.Text)
    prompt = db.Column(db.Text) #added some dummy integer columns to test stuff first
    answer = db.Column(db.Text)
    solution = db.Column(db.Text)
    question = db.Column(db.Text)

class Module(db.Model):
    __tablename__='module'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique = True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)

class UserActivity(db.Model):
    __tablename__='userActivity'
    user_activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    count_submitted = db.Column(db.Integer)
    is_completed = db.Column(db.Integer)

class Submission(db.Model):
    __tablename__='submission'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class ActivityDependency(db.Model):
    __tablename__='activityDependency'
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer, db.ForeignKey('activity.id')) #integer id of the parent activity
    child = db.Column(db.Integer, db.ForeignKey('activity.id'))

class ModuleDependency(db.Model):
    __tablename__='moduleDependency'
    id = db.Column(db.Integer, primary_key=True)
    parent = db.Column(db.Integer, db.ForeignKey('module.id')) #integer id of the parent module
    child = db.Column(db.Integer, db.ForeignKey('module.id'))
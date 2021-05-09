from datetime import datetime, timedelta
from flask_login import UserMixin 
from werkzeug.security import generate_password_hash, check_password_hash
from app import login, db

# allows login to get User from db given the id
@login.user_loader
def load_user(id):
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
    is_admin = db.Column(db.Integer, default=0)

    user_activities = db.relationship("UserActivity", backref='User', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_activity(self, activity):
        if isinstance(activity, Activity):
            return UserActivity.query.filter_by(user_id=self.id, activity_id=activity.id).first()
    
    def submit_one(self):
        self.total_submissions += 1
    
    def add_loc(self, loc):
        if isinstance(loc, int) and 0 < loc < 10000:
            self.lines_of_code += loc

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
    prefill = db.Column(db.Text)

    # statistics
    # This needs to be server default because they are created manually
    times_submitted = db.Column(db.Integer, default=0)
    times_right = db.Column(db.Integer, default=0)
    # % of of users attempted this 

    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    dependencies = db.relationship("ActivityDependency", backref='childActivity', foreign_keys="ActivityDependency.child", lazy=True)
    parent_of = db.relationship("ActivityDependency", backref='parentActivity', foreign_keys="ActivityDependency.parent", lazy=True)

    def __repr__(self):
        return f"<Activity {self.name}"
    
    # Make a UserActivity for the given user
    def makeUserActivity(self, user):
        newUserActivity = UserActivity(user_id=user.id, activity_id=self.id)
        db.session.add(newUserActivity)
        db.session.commit()
        return newUserActivity
    
    # Get UserActivity from this activity
    def getUserActivity(self, user):
        return UserActivity.query.filter_by(user_id=user.id, activity_id=self.id).first()

class Module(db.Model):
    __tablename__='module'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique = True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)

    activities = db.relationship("Activity", lazy=True,
        backref = 'module')

    dependencies = db.relationship("ModuleDependency", foreign_keys="ModuleDependency.child", lazy=True)
    parent_of = db.relationship("ModuleDependency", foreign_keys="ModuleDependency.parent", lazy=True)

class UserActivity(db.Model):
    __tablename__='userActivity'
    user_activity_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'))
    count_submitted = db.Column(db.Integer)
    is_completed = db.Column(db.Integer)
    saved = db.Column(db.Text)

    activity = db.relationship("Activity",lazy=True, foreign_keys=[activity_id])
    def __repr__(self):
        return f"<UserActivity {self.activity.name}>"
    
    def set_completion(self, completion):
        self.is_completed = completion
    
    def save_code(self, code):
        self.saved = code

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
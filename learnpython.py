from app import app, db
from app.models import User, Activity, Module, UserActivity, Submission, ActivityDependency, ModuleDependency

# this allows us to use `flask shell` in terminal to help test better
@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Activity':Activity, 'Module':Module,
    'UserActivity':UserActivity, 'Submission':Submission, 'ActivityDependency':ActivityDependency,
    'ModuleDependency':ModuleDependency}
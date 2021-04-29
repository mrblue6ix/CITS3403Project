#add os version to requirements???
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #have to set secret key as system variable in terminal
    # export SECRET_KEY='this_is_the_secret_key'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #also store database key, locations,... here
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE.URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

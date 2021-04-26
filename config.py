#add os version to requirements???
import os

class Config(object):
    #have to set secret key as system variable in terminal
    # export SECRET_KEY='this_is_the_secret_key'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    #also store database key, locations,... here
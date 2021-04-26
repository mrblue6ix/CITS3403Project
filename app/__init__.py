# initialization file for the app
from flask import Flask

app = Flask(__name__)
#change secret key to something else, it is unsafe to have it like below
app.config['SECRET_KEY'] = 'this_is_a_temp_secret_key'
from app import routes

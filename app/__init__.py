# initialization file for the app
from flask import Flask

app = Flask(__name__)
#change secret key to something else, it is unsafe to have it like below
#app.config['SECRET_KEY'] = 'this_is_a_temp_secret_key'
#below gets config from the config file
app.config.from_object(Config)
from app import routes

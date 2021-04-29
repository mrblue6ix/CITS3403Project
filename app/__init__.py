# initialization file for the app
from flask import Flask
from config import config
from flask_sqlalchemy import flask_sqlalchemy
from flask_migrate import Migrate

#add db stuff to config file to make this do stuff
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import routes, models

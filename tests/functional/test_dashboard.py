from app import app

from flask import Flask
from config import TestConfig
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app import routes, models

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# def test_dashboard():
#     app = Flask("learnpython")
#     login = LoginManager(app)
# 
#     app.config.from_object(TestConfig)
#     metadata = MetaData(naming_convention=convention)
#     db = SQLAlchemy(app, metadata=metadata)
#     migrate = Migrate(app, db)
# 
#     # this is required as SQLite does not support ALTER of constraints
#     with app.app_context():
#         if db.engine.url.drivername == "sqlite":
#             migrate.init_app(app, db, render_as_batch=True)
#         else:
#             migrate.init_app(app, db)
#     
#     with app.test_client() as test_client:
#         resp = test_client.get("/index")
#         assert resp.status_code == 200
#         print(resp.data)
import logging
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from config import ActiveConfig

# initialize and configure the flask server
app = Flask(__name__)
app.config.from_object(ActiveConfig)

# set up logger level
if not app.debug:
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

# open and intialize or read the database
db = SQLAlchemy(app)

from application import models, views
from application.utils.initializers import init_db, init_admin, init_login, init_app

init_app(app)
init_db(db)
init_admin(app, db)
init_login(app)


def main():
    app.run(use_reloader=False)

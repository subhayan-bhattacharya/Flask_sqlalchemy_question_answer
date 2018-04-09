from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from os import urandom
from config import BaseConfig
import logging.config
app = Flask(__name__)
app.config.from_object(BaseConfig)

db = SQLAlchemy(app)

from views import *

log_config = app.config['LOGGING_CONFIG']
logging.config.dictConfig(log_config)
logger = logging.getLogger("question_answer_app")
app.logger.handlers = logger.handlers
app.logger.setLevel(logger.level)

@app.before_first_request
def create_tables():
    db.create_all()





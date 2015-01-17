from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import assets
import os

app = Flask(__name__)
app.config.from_object('config')

env = assets.Environment(app)

env.load_path = [
    os.path.join(os.path.dirname(__file__), '../bower_components'),
]


env.register(
    'style',
    assets.Bundle(
        'materialize/dist/css/materialize.min.css',
        output='style.css'
    )
)

db = SQLAlchemy(app)

from app import views, models


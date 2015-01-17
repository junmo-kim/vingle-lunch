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
        filters='cssutils',
        output='style.css'
    )
)

env.register(
    'script',
    assets.Bundle(
        'jquery/dist/jquery.min.js',
        'materialize/dist/js/materialize.min.js',
        filters='jsmin',
        output='script.js'
    )
)

db = SQLAlchemy(app)

from app import views, models


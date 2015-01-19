from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import assets
import os

app = Flask(__name__)
app.config.from_object('config')

env = assets.Environment(app)

env.load_path = [
    os.path.join(os.path.dirname(__file__), '../bower_components'),
    os.path.join(os.path.dirname(__file__), 'assets'),
]

env.register(
    'style',
    assets.Bundle(
        'materialize/dist/css/materialize.min.css',
            assets.Bundle(
            'scss/main.scss',
            filters='scss',
        ),
        filters='cssutils',
        output='css/style.css'
    )
)

env.register(
    'script',
    assets.Bundle(
        'jquery/dist/jquery.min.js',
        'materialize/dist/js/materialize.min.js',
        'jquery.countdown/dist/jquery.countdown.min.js',
        'js/main.js',
        filters='jsmin',
        output='js/script.js'
    )
)

db = SQLAlchemy(app)

from app import views, models


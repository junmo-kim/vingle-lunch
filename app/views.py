from app import app
from app.models import User
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

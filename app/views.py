from app import app, db
from app.models import Team, User, Group, Lunch
from app.forms import TeamForm, UserForm, LunchDataForm
from flask import render_template, redirect
from random import shuffle
import math
import json
import datetime
import operator

@app.route('/')
@app.route('/index')
def index():
    users = User.query.filter(User.deactivate!=True).order_by(User.eat.desc()).all()
    return render_template('users.html', team=None, users=users)

@app.route('/teams/new', methods=('GET', 'POST'))
def new_team():
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(form.title.data, form.key.data)
        db.session.add(team)
        db.session.commit()
        return redirect('/')
    return render_template('new_team.html', form=form)

@app.route('/teams/<int:team_id>')
def team(team_id):
    team = Team.query.get(team_id)
    return render_template('users.html', team=team, users=team.users.order_by(User.eat.desc()))

@app.route('/users')
def users():
    return redirect('/')

@app.route('/users/new', methods=('GET', 'POST'))
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.team.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('edit_user.html', form=form, user=None)

@app.route('/users/<int:user_id>/edit', methods=('GET', 'POST'))
def edit_user(user_id):
    form = UserForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.team = form.team.data
        db.session.commit()
        return redirect('/')
    form.name.data = user.name
    form.team.data = user.team
    return render_template('edit_user.html', form=form, user=user)

@app.route('/users/<int:user_id>')
def user(user_id):
    user = User.query.get(user_id)
    return user.name

@app.route('/users/<int:user_id>/<state>')
def activate_user(user_id, state):
    user = User.query.get(user_id)
    if state == 'activate':
        user.deactivate = False
    elif state == 'deactivate':
        user.deactivate = True
    db.session.commit()
    return redirect('/')

@app.route('/users/<int:user_id>/eat/<eat>')
def eat_lunch(user_id, eat):
    user = User.query.get(user_id)
    if eat == 'yes':
        user.eat = True
    elif eat == 'next':
        user.eat = False
    db.session.commit()
    return redirect('/')

@app.route('/lunches')
def lunches():
    lunches = Lunch.query.all()
    return render_template('lunches.html', lunches=lunches)

MAX_MEMBER = 5
@app.route('/lunches/new', methods=('GET', 'POST'))
def create_lunch():
    form = LunchDataForm()
    if form.validate_on_submit():
        groups_data = json.loads(form.data.data)
        lunch = Lunch()
        lunch.date = datetime.datetime.now()
        for group_data in groups_data:
            group = Group()
            group.lunch = lunch
            for user_id in group_data:
                user = User.query.get(user_id)
                group.users.append(user)
            db.session.add(group)
        db.session.add(lunch)
        db.session.commit()
        return redirect('/lunches/%d' % lunch.id)
    else:
        users = User.query.filter(User.deactivate!=True, User.eat!=False).all()
        shuffle(users)
        group_count = math.ceil(len(users) / MAX_MEMBER)

        groups = []
        groups_data = []
        for i in range(group_count):
            groups.append(dict(users=[]))
            groups_data.append([])

        for index, user in enumerate(users):
            group_index = index % group_count 
            groups[group_index].get('users').append(user)
            groups_data[group_index].append(user.id)
        return render_template('lunch.html', form=form, date=datetime.datetime.now(), groups=groups, groups_data=json.dumps(groups_data))

@app.route('/lunches/<int:lunch_id>')
def lunch(lunch_id):
    lunch = Lunch.query.get(lunch_id)
    return render_template('lunch.html', date=lunch.date, groups=lunch.groups)

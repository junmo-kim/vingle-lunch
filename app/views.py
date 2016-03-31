from app import app, db
from app.models import Team, User, Group, Lunch
from app.forms import TeamForm, UserForm, LunchDataForm
from flask import render_template, redirect, request, send_from_directory, url_for
from random import shuffle
import math
import json
import datetime
import sys

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/')
def index():
    users = User.active_users()

    admin = False
    if request.args.get('admin', '') == 'true':
        admin = True

    return render_template('users.html', team=None, users=users, admin=admin)

@app.route('/teams/<int:team_id>')
def team(team_id):
    team = Team.query.get(team_id)
    users = team.users.order_by(User.eat.desc()).filter(User.deactivate!=True)
    return render_template('users.html', team=team, users=users)

@app.route('/teams/<int:team_id>/edit', methods=('GET', 'POST'))
def edit_team(team_id):
    form = TeamForm()
    team = Team.query.get(team_id)
    if form.validate_on_submit():
        team.key = form.key.data
        team.title = form.title.data
        db.session.commit()
        return redirect(url_for('team', team_id=teamd_id))
    form.key.data = team.key
    form.title.data = team.title
    return render_template('edit_team.html', form=form, team=team)

@app.route('/teams/new', methods=('GET', 'POST'))
def new_team():
    form = TeamForm()
    if form.validate_on_submit():
        team = Team(form.title.data, form.key.data)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_team.html', form=form)

@app.route('/users')
def users():
    return redirect(url_for('index'))

@app.route('/users/new', methods=('GET', 'POST'))
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.team.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_user.html', form=form, user=None)

@app.route('/users/deactivated')
def deactivated_users():
    users = User.query.filter_by(deactivate=True)
    return render_template('users.html', team=None, users=users)

@app.route('/users/<int:user_id>')
def user(user_id):
    user = User.query.get(user_id)
    groups = user.recent_groups()
    return render_template('user.html', user=user, recent_groups=groups)

@app.route('/users/<int:user_id>/edit', methods=('GET', 'POST'))
def edit_user(user_id):
    form = UserForm()
    user = User.query.get(user_id)
    if form.validate_on_submit():
        user.name = form.name.data
        user.team = form.team.data
        if (form.gender.data):
            user.gender = form.gender.data
        db.session.commit()
        return redirect(url_for('index'))
    form.name.data = user.name
    form.team.data = user.team
    form.gender.data = user.gender

    admin = False
    if request.args.get('admin', '') == 'true':
        admin = True

    return render_template('edit_user.html', form=form, user=user, admin=admin)

@app.route('/users/<int:user_id>/<state>')
def activate_user(user_id, state):
    user = User.query.get(user_id)
    if state == 'activate':
        user.deactivate = False
        db.session.commit()
        return redirect(url_for('index'))
    elif state == 'deactivate':
        user.deactivate = True
        db.session.commit()
        return redirect(url_for('deactivated_users'))

@app.route('/users/<int:user_id>/eat/<eat>')
def eat_lunch(user_id, eat):
    user = User.query.get(user_id)
    if eat == 'yes':
        user.eat = True
    elif eat == 'next':
        user.eat = False
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/lunches')
def lunches():
    lunches = Lunch.query.order_by(Lunch.date.desc()).all()
    return render_template('lunches.html', lunches=lunches)

MAX_MEMBER = 5
def compute_penalty(user, users, past_lunches):
    penalty = float(math.pow(2.0, len(users))) / 32.0
    for index, lunch in enumerate(past_lunches):
        group = user.group_in_lunch(lunch)
        if group:
            for colleague in users:
                colleague_group = colleague.group_in_lunch(lunch)
                if colleague_group and group.id == colleague_group.id:
                    penalty += 1.0 / float(math.pow(2.0, index + 1))

    for colleague in users:
        if user.gender == colleague.gender:
            penalty += 1.0 / 8.0
        if user.team == colleague.team:
            penalty += 1.0 / 8.0

    return penalty

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

        all_users = User.query.all()
        for user in all_users:
            user.eat = True
        db.session.commit()
        return redirect(url_for('lunch', lunch_id=lunch.id))
    else:
        users = User.query.filter(User.deactivate!=True, User.eat!=False).all()
        shuffle(users)
        group_count = math.ceil(len(users) / MAX_MEMBER)

        past_lunches = Lunch.query.order_by(Lunch.date.desc()).limit(3)

        groups = []
        groups_data = []
        for i in range(group_count):
            groups.append(dict(users=[], penalties=[]))
            groups_data.append([])

        for index, user in enumerate(users):
            target_group = None
            target_index = 0
            min_penalty = sys.maxsize
            for index, group in enumerate(groups):
                if len(group.get('users')) >= MAX_MEMBER:
                    continue

                penalty = compute_penalty(user, group.get('users'), past_lunches)
                if penalty < min_penalty:
                    min_penalty = penalty
                    target_group = group
                    target_index = index
                if penalty == 0:
                    break
            target_group.get('users').append(user)
            groups_data[target_index].append(user.id)

        for group in groups:
            for user in group.get('users'):
                penalty = compute_penalty(user, group.get('users'), past_lunches)
                group.get('penalties').append(penalty)

        return render_template('lunch.html', form=form, date=datetime.datetime.now(), groups=groups, groups_data=json.dumps(groups_data))

@app.route('/lunches/<int:lunch_id>')
def lunch(lunch_id):
    lunch = Lunch.query.get(lunch_id)
    return render_template('lunch.html', date=lunch.date, groups=lunch.groups)

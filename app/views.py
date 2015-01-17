from app import app, db
from app.models import Team, User
from app.forms import TeamForm, UserForm
from flask import render_template, redirect

@app.route('/')
@app.route('/index')
def index():
    teams = Team.query.all()
    users = User.query.all()
    return render_template('index.html', teams=teams, users=users)

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
    return team.title

@app.route('/users/<int:user_id>')
def user(user_id):
    user = User.query.get(user_id)
    return user.name

@app.route('/users/new', methods=('GET', 'POST'))
def new_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(form.name.data, form.team.data)
        db.session.add(user)
        db.session.commit()
        return redirect('/')
    return render_template('new_user.html', form=form)

@app.route('/users/<int:user_id>/edit', methods=('GET', 'POST'))
def edit_user(user_id):
    form = UserForm()
    user = User.query.get(user_id)
    form.team.data = user.team
    if form.validate_on_submit():
        user.name = form.name.data
        user.team = form.team.data
        db.session.commit()
        return redirect('/')
    return render_template('edit_user.html', form=form, user=user)


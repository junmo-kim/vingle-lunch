from app import db
from app.models import User, Team

with open('teams.txt', 'r') as f:
    for line in f:
        team_data = line.split('\t')
        if len(team_data) != 2:
            continue
        team = Team(team_data[1], team_data[0])
        db.session.add(team)

with open('users.txt', 'r') as f:
    for line in f:
        user_data = line.split('\t')
        if len(user_data) != 2:
            continue
        team = Team.query.filter_by(key=user_data[1]).first()
        user = User(user_data[0], team)
        db.session.add(user)

db.session.commit()

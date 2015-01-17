from app import db
from app.models import User, Team, Lunch, Group
import json

teams_json=open('legacy/teams.json')
teams_data = json.load(teams_json)
for team_data in teams_data:
    team = Team(team_data[1], team_data[0])
    print ('[%s] %r' % (team.key, team.title))
    db.session.add(team)
teams_json.close()
db.session.commit()
print('\n')

users_json=open('legacy/users.json')
users_data = json.load(users_json)
for user_data in users_data:
    team = Team.query.filter_by(key=user_data[1]).first()
    user = User(user_data[0], team)
    print ('[%s] %r' % (user.team.key, user.name))
    db.session.add(user)
users_json.close()
db.session.commit()
print('\n')

lunches_json=open('legacy/lunches.json')
lunches_data = json.load(lunches_json)
for lunch_data in lunches_data:
    lunch = Lunch()
    for group_data in lunch_data:
        group = Group()
        group.lunch = lunch
        for user_id in group_data:
            user = User.query.get(user_id)
            group.users.append(user)
        db.session.add(group)
    db.session.add(lunch)
lunches_json.close()
db.session.commit()

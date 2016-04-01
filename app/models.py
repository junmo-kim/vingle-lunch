from app import db
from werkzeug.utils import cached_property
from werkzeug.contrib.cache import SimpleCache
import random

cache = SimpleCache()


user_team = db.Table(
    'user_team',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id')),
)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    deactivate = db.Column(db.Boolean, index=True)
    eat = db.Column(db.Boolean)
    gender = db.Column(db.String(1))

    teams = db.relationship('Team', secondary=user_team, backref='users', lazy='dynamic')

    def __init__(self, name, team=None):
        self.name = name
        self.team = team
        self.deactivate = False
        self.eat = True

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.name)

    @classmethod
    def active_users(self):
        return self.query.filter(self.deactivate != True).order_by(self.eat.desc()).all()

    def recent_groups(self, max_number=3):
        groups = Group.query.filter(Group.users.any(id=self.id))\
                                          .order_by(Group.lunch_id.desc())\
                                          .limit(max_number)
        return groups

    def group_in_lunch_cache_key(self, lunch):
        return 'group_in_lunch_%d_%d' % (self.id, lunch.id)

    def group_in_lunch(self, lunch):
        group = cache.get(self.group_in_lunch_cache_key(lunch))
        if group == False:
            return None
        elif group:
            return group
        else:
            try:
                group = Group.query.filter_by(lunch=lunch).filter(Group.users.any(id=self.id)).all()[0]
            except:
                group = False
            cache.set(self.group_in_lunch_cache_key(lunch), group, timeout=8 * 24 * 60)
            return group

    @property
    def all_teams(self) -> set:
        teams = self.teams
        all_teams = set(teams)

        for team in teams:
            parent = team
            while parent.parent:
                parent = parent.parent
                all_teams.add(parent)

        return all_teams

    @property
    def repr_team(self):
        all_teams = self.all_teams

        teams_by_depth = dict()
        for team in all_teams:
            existing = teams_by_depth.get(team.depth)
            if existing:
                teams_by_depth.get(team.depth).add(team)
            else:
                teams_by_depth[team.depth] = {team}

        last_team = None
        for key in sorted(teams_by_depth.keys()):
            teams_in_depth = teams_by_depth.get(key)
            if len(teams_in_depth) != 1:
                if key == 0:
                    last_team = random.choice(tuple(teams_in_depth))
                break
            last_team = random.choice(tuple(teams_in_depth))
        return last_team


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    key = db.Column(db.String(32), index=True, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    parent = db.relationship('Team', remote_side=[id], backref='children')
    inactive = db.Column(db.Boolean, default=True)

    def __init__(self, title, key):
        self.title = title
        self.key = key

    def __repr__(self):
        return '<Team [%r]: %r>' % (self.key, self.title)

    def __str__(self):
        return self.title

    @property
    def depth(self):
        parent = self
        depth = 0
        while parent.parent:
            depth += 1
            parent = parent.parent
        return depth

user_group = db.Table(
    'user_group',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)

    users = db.relationship('User', secondary=user_group, backref='groups', lazy='dynamic')

    lunch_id = db.Column(db.Integer, db.ForeignKey('lunches.id'))


class Lunch(db.Model):
    __tablename__ = 'lunches'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    groups = db.relationship('Group', backref='lunch', lazy='dynamic')

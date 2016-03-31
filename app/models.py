from app import db
from werkzeug.contrib.cache import SimpleCache
from marshmallow import Schema, fields, ValidationError, pre_load
cache = SimpleCache()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    deactivate = db.Column(db.Boolean, index=True)
    eat = db.Column(db.Boolean)
    gender = db.Column(db.String(1))

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', backref=db.backref('users', lazy='dynamic'))

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


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    deactivate = fields.Boolean()
    eat = fields.Boolean()
    team = fields.Nested('TeamSchema', exclude=('users', ))
    recent_groups = fields.Method('recent_groups', dump_only=True)

    def recent_groups(self, obj):
        return obj.recent_groups()


user_schema = UserSchema()


def user_serializer(instance):
    return user_schema.dump(instance).data


def user_deserializer(data):
    return user_schema.load(data).data


class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    key = db.Column(db.String(32), index=True, unique=True)

    def __init__(self, title, key):
        self.title = title
        self.key = key

    def __repr__(self):
        return '<Team [%r]: %r>' % (self.key, self.title)

    def __str__(self):
        return self.title

user_group = db.Table(
    'user_group',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)


class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    key = fields.Str()
    users = fields.Nested('UserSchema', many=True, exclude=('team', ))


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

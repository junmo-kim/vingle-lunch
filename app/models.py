from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    deactivate = db.Column(db.Boolean, index=True)
    eat = db.Column(db.Boolean)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', backref=db.backref('teams', lazy='dynamic'))

    def __init__(self, name, team=None):
        self.name = name
        self.team = team
        self.deactivate = False
        self.eat = True

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.name)

    def past_groups(self, max_number=3):
        groups = Group.query.filter(Group.users.any(id=self.id))\
                                          .order_by(Group.lunch_id.desc())\
                                          .limit(max_number)
        return groups

    def group_in_lunch(self, lunch):
        try:
            group = Group.query.filter_by(lunch=lunch).filter(Group.users.any(id=self.id)).all()[0]
        except:
            return None
        return  group

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    key = db.Column(db.String(32), index=True, unique=True)

    users = db.relationship('User', backref='users', lazy='dynamic')

    def __init__(self, title, key):
        self.title = title
        self.key = key

    def __repr__(self):
        return '<Team [%r]: %r>' % (self.key, self.title)

    def __str__(self):
        return self.title

user_group = db.Table('user_group',
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)

    users = db.relationship('User', secondary=user_group,
      backref=db.backref('groups', lazy='dynamic'))

    lunch_id = db.Column(db.Integer, db.ForeignKey('lunches.id'))
    lunch = db.relationship('Lunch', backref=db.backref('lunches', lazy='dynamic'))

class Lunch(db.Model):
    __tablename__ = 'lunches'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    groups = db.relationship('Group', backref='groups', lazy='dynamic')

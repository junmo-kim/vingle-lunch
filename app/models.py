from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)

    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    team = db.relationship('Team', backref=db.backref('teams', lazy='dynamic'))

    def __init__(self, name, team=0):
        self.name = name
        self.team = team

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.name)

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


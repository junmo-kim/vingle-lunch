from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))

    def __repr__(self):
        return '<User %r: %r>' % (self.id, self.name)

class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), unique=True)
    key = db.Column(db.String(32), index=True, unique=True)

    def __repr__(self):
        return '<Team [%r]: %r>' % (self.key, self.title)


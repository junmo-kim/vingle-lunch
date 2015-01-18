from flask_wtf import Form
from wtforms import StringField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from app.models import Team

class TeamForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    key = StringField('Key', validators=[DataRequired()])

def enabled_teams():
    return Team.query.all()

class UserForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    team = QuerySelectField('Team', query_factory=enabled_teams, allow_blank=True, blank_text='Choose your team')
    gender = StringField('gender')

class LunchDataForm(Form):
	data = HiddenField('Data', validators=[DataRequired()])

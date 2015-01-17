from flask_wtf import Form
from wtforms import StringField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from app.models import Team

class TeamForm(Form):
    title = StringField('title', validators=[DataRequired()])
    key = StringField('key', validators=[DataRequired()])

def enabled_teams():
    return Team.query.all()

class UserForm(Form):
    name = StringField('name', validators=[DataRequired()])
    team = QuerySelectField(query_factory=enabled_teams, allow_blank=True)

class LunchDataForm(Form):
	data = HiddenField('data', validators=[DataRequired()])

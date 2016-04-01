from flask_wtf import Form
from wtforms import StringField, HiddenField, BooleanField
from wtforms.fields import SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Optional
from app.models import Team

def enabled_teams():
    return Team.query.all()


class TeamForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    key = StringField('Key', validators=[DataRequired()])
    inactive = BooleanField('Inactive')
    parent = QuerySelectField('Parent Team', query_factory=enabled_teams, allow_blank=True,
                              blank_text='Choose parent team')


class UserForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    teams = QuerySelectMultipleField('Teams', query_factory=enabled_teams, allow_blank=False,
                                     blank_text='Choose your teams')
    gender = SelectField('Gender', validators=[Optional()],
                         choices=[(None, 'Not set'), ('m', 'Male'), ('f', 'Female'), ('q', 'Other')])


class LunchDataForm(Form):
    data = HiddenField('Data', validators=[DataRequired()])

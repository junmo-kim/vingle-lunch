from app import app, db
from .models import User, Team, Lunch, Group
from flask.ext.restless import APIManager
from marshmallow import Schema, fields, ValidationError, pre_load

manager = APIManager(app, flask_sqlalchemy_db=db)


def serializer(schema: Schema):
    return lambda instance: schema.dump(instance).data


def deserialize(schema: Schema):
    return lambda data: schema.load(data).data


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    deactivate = fields.Boolean()
    eat = fields.Boolean()
    team = fields.Nested('TeamSchema', exclude=('users', ))
    recent_groups = fields.Method('get_recent_groups', dump_only=True)

    def get_recent_groups(self, obj: User) -> object:
        return list(map(lambda group: serializer(group_schema)(group), obj.recent_groups()))

user_schema = UserSchema()


class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    key = fields.Str()
    users = fields.Nested('UserSchema', many=True, exclude=('team', 'recent_groups'))

team_schema = TeamSchema()


class GroupSchema(Schema):
    id = fields.Int(dump_only=True)
    users = fields.Nested('UserSchema', many=True, dump_only=True, exclude=('recent_groups', ))
    lunch = fields.Nested('LunchSchema', only=('id', 'date'), dump_only=True)

group_schema = GroupSchema()


class LunchSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    groups = fields.Nested(GroupSchema, many=True, dump_only=True, exclude=('lunch', ))

lunch_schema = LunchSchema()

manager.create_api(User, methods=['GET', 'POST', 'DELETE'],
                   serializer=serializer(user_schema), deserializer=deserialize(user_schema))
manager.create_api(Team, methods=['GET'],
                   serializer=serializer(team_schema), deserializer=deserialize(team_schema))
manager.create_api(Lunch, methods=['GET'],
                   serializer=serializer(lunch_schema), deserializer=deserialize(lunch_schema))

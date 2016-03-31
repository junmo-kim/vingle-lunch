from app import app, db
from .models import User, Team, Lunch, Group
from flask.ext.restless import APIManager
from marshmallow import Schema, fields, ValidationError, pre_load

manager = APIManager(app, flask_sqlalchemy_db=db)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    deactivate = fields.Boolean()
    eat = fields.Boolean()
    team = fields.Nested('TeamSchema', exclude=('users', ))
    recent_groups = fields.Method('get_recent_groups', dump_only=True)

    def get_recent_groups(self, obj: User) -> object:
        return list(map(lambda g: group_serializer(g), obj.recent_groups()))

user_schema = UserSchema()


def user_serializer(instance):
    return user_schema.dump(instance).data


def user_deserializer(data):
    return user_schema.load(data).data


class TeamSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    key = fields.Str()
    users = fields.Nested('UserSchema', many=True, exclude=('team', ))

team_schema = TeamSchema()


def team_serializer(instance: Team) -> dict:
    return team_schema.dump(instance).data


def team_deserializer(data: dict) -> Team:
    return team_schema.load(data).data


class GroupSchema(Schema):
    id = fields.Int(dump_only=True)
    users = fields.Nested('UserSchema', many=True, dump_only=True, exclude=('recent_groups', ))
    lunch_id = fields.Int(dump_only=True)

group_schema = GroupSchema()


def group_serializer(instance: Group) -> dict:
    return group_schema.dump(instance).data


def group_deserializer(data: dict) -> Group:
    return group_schema.load(data).data


class LunchSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(dump_only=True)
    groups = fields.Nested(GroupSchema, many=True, dump_only=True)

lunch_schema = LunchSchema()


def lunch_serializer(instance: Lunch) -> dict:
    return lunch_schema.dump(instance).data


def lunch_deserializer(data: dict) -> Lunch:
    return lunch_schema.load(dict).data


manager.create_api(User, methods=['GET', 'POST', 'DELETE'],
                   serializer=user_serializer, deserializer=user_deserializer)
manager.create_api(Team, methods=['GET'],
                   serializer=team_serializer, deserializer=team_deserializer)
manager.create_api(Lunch, methods=['GET'],
                   serializer=lunch_serializer, deserializer=lunch_deserializer)

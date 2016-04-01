from app import app, db
from .models import User, Team, Lunch, Group
from flask import request
from flask.views import MethodView
from flask.json import jsonify
from marshmallow import Schema, fields, ValidationError, pre_load


def serializer(schema: Schema):
    return lambda instance, many=None: schema.dump(instance, many=many).data


def deserializer(schema: Schema):
    return lambda data, many=None: schema.load(data, many=many).data


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


class UserAPI(MethodView):
    def get(self, user_id):
        if user_id:
            user = User.query.get(user_id)
            return jsonify(serializer(user_schema)(user))
        else:
            if request.args.get('all'):
                users = User.query.all()
            else:
                users = User.active_users()
            return jsonify(dict(
                data=serializer(user_schema)(users, many=True)
            ))


class UserEatAPI(MethodView):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            if user.eat:
                return jsonify(dict(data=True))
            else:
                return jsonify(dict(error="Eat Not Found")), 404
        else:
            return jsonify(dict(error="User Not Found")), 404

    def put(self, user_id):
        user = User.query.get(user_id)
        if user:
            user.eat = True
            db.session.commit()
            return jsonify(dict(success=True))
        else:
            return jsonify(dict(error="User Not Found")), 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            user.eat = False
            db.session.commit()
            return jsonify(dict(success=True))
        else:
            return jsonify(dict(error="User Not Found")), 404


user_view = UserAPI.as_view('user_api')
app.add_url_rule('/api/users/', defaults={'user_id': None},
                 view_func=user_view, methods=['GET', ])
app.add_url_rule('/api/users/', view_func=user_view, methods=['POST', ])
app.add_url_rule('/api/users/<int:user_id>', view_func=user_view,
                 methods=['GET'])

user_eat_view = UserEatAPI.as_view('user_eat_api')
app.add_url_rule('/api/users/<int:user_id>/eat', view_func=user_eat_view,
                 methods=['GET', 'PUT', 'DELETE'], endpoint='user_eat_api')


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

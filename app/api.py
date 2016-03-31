from app import app, db
from .models import User, user_serializer, user_deserializer, Team, Lunch
from flask.ext.restless import APIManager

manager = APIManager(app, flask_sqlalchemy_db=db)

manager.create_api(User, methods=['GET', 'POST', 'DELETE'],
                   serializer=user_serializer, deserializer=user_deserializer)
manager.create_api(Team, methods=['GET'])
manager.create_api(Lunch, methods=['GET'])

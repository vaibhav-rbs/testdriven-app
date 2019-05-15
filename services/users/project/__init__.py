import os
from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config.from_object('project.config.DevelopmentConfig')
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(Self, username, email):
        self.username = username
        Self.email = email
        
class UserPing(Resource):
    def get(self):
        return {
            'status':'sucess',
            'message':'pong!'
        }
api.add_resource(UserPing, '/users/ping')
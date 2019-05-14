import os
from flask import Flask, jsonify
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

app.config.from_object('project.config.DevelopmentConfig')
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

class UserPing(Resource):
    def get(self):
        return {
            'status':'sucess',
            'message':'pong!'
        }
api.add_resource(UserPing, '/users/ping')
from flask import Blueprint,request

from flask_restful import Resource, Api

from project import db
from project.api.models import User
from sqlalchemy import exc


users_blueprint = Blueprint('users',__name__)
api = Api(users_blueprint)

class UsersPing(Resource):
    def get(self):
        return {
            'status':'success',
            'message':'pong!'
        }
class UserList(Resource):
    def post(self):
        post_data = request.get_json()
        response_object = {
            'status':'fail',
            'message':'Invalid payload.'
        }
        if not post_data:
            return response_object, 400
        username = post_data.get('username')
        email = post_data.get('email')
        if not username or not email:
             return response_object, 400
        try:
            user = User.query.filter_by(email=email).first()
            if not user:
                db.session.add(User(username=username, email=email))
                db.session.commit()
                response_object = {
                    'status':'success',
                    'message':f'{email} was added!'
                }
                return response_object, 201
            else:
                response_object['message'] = 'Sorry. That email already exists.'
                return response_object, 400
        except exc.IntegrityError:
            db.session.rollback()

    def get(self):
        response_object = {
            'status':'success',
            'data':{
                'users':[user.to_json() for user in User.query.all()]
            }
        }
        return response_object,200
        



class Users(Resource):
    def get(self,id):
        response_object = {
        'status':'fail',
        'message':'User does not exits'
        }
        try:
            user  = User.query.filter_by(id=int(id)).first()
            if not user:
                return response_object, 404
            else:
                response_object = {
                    'status':'success',
                    'data':{
                        'id' : user.id,
                        'username':user.username,
                        'email':user.email,
                        'active':user.active
                    }
                }
                return response_object, 200
        except ValueError:
            return response_object, 404
api.add_resource(UsersPing,'/users/ping')
api.add_resource(UserList,'/users')
api.add_resource(Users,'/users/<id>')
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                type=str,
                required=True,
                help="This field cannot be left blank!"
    )
        
    parser.add_argument('password',
                type=str,
                required=True,
                help="This field cannot be left blank!"
    )
        
    def post(self):
        data = UserRegister.parser.parse_args()

        
        if UserModel.find_by_username(data['username']):
            return {"message":"Username already exists"},400
        
        user = UserModel(**data)
        user.save_to_db()

        return{"message":"User created successfully."}, 201


class UserReview(Resource):
    def get(self):
        
            return {'username':[user.json() for user in UserModel.query.all()]}


class User(Resource):
    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user : 
            return {'message':'User not found'}, 404
        return user.json()

    def delete(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if not user : 
            return {'message':'User not found'}, 404
        user.delete_from_db()
        return{'message': 'user deleted'}
    
        
        
    

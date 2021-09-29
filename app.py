
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, UserReview,User,UserLogin
from resources.item import Item,ItemList
from resources.store import Store,StoreList
from db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
app.config['PROPAGATE_EXCEPTIONS']= True
app.secret_key = 'yahia' #app.config['JWT_SECRET_KEY']='YAHIA'
api= Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt= JWTManager(app) #/auth
@jwt.additional_claims_loader 
def additional_claims(identity):
    if identity == 1:
        return{'is_admin': True}
    return{'is_admin':False}



api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserReview,'/review')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserLogin,'/login')
if __name__ == '__main__':
    app.run(port=5000,debug = True)

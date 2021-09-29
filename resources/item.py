from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import jwt_required, get_jwt,get_jwt_identity
from sqlalchemy.orm import query
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
            type=float,
            required=True,
            help="This field cannot be left blank!"
        )
    parser.add_argument('store_id',
            type=int,
            required=True,
            help="Every item need a Store id"
        )

    @jwt_required()
    def get(self, name):

            item = ItemModel.find_by_name(name)
            if item:
                return item.json()
        
            return {'message':'Item not found'},404

    @jwt_required(fresh=True)
    def post(self,name):

            if ItemModel.find_by_name(name):
                return{'message':"An item with name'{}'already exists.".format(name)}, 400

            data = Item.parser.parse_args()
            
            item =ItemModel(name ,**data)
            try:
                item.save_to_db()
            except:
                return {"message":"An error ocurred inserting the item"}, 500
           
            return item.json(), 201
    
    @jwt_required()
    def delete(self,name):
            claims = get_jwt()
            if not claims==['is_admin']:
                return {'message':'Admin previlege required'}
            item = ItemModel.find_by_name(name)
            if item:
                item.delete_from_db()
                return{'message':'item deleted'}
            return{'message':'item not found'}
            
    def put(self,name):
        data = Item.parser.parse_args()
        
        item = ItemModel.find_by_name(name)
    
        if item is None:
          item = ItemModel(name,**data)

        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
            user_id = get_jwt_identity()
            items=[item.json() for item in ItemModel.find_all()]
            if user_id:
                return {'items':items},200
            return{
                'items':[item['name'] for item in items],
                'message':'More data avaliable if you log in'
                }
            #return{'items':list(map(lambda x :x.json(),ItemModel.query.all()))} same as first
from flask_restful import Resource, abort, reqparse
from flask import jsonify
from data import db_session, objects, users


def abort_if_obj_not_found(obj_id):
    session = db_session.create_session()
    obj = session.query(objects.Object).get(obj_id)
    if not obj:
        abort(404, message=f"Ошибка 404 \n Объект {obj_id} не найден")


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('category')
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('price', required=True, type=int)
parser.add_argument('description', required=True)
parser.add_argument('sold')


class ObjResource(Resource):
    def get(self, obj_id):
        abort_if_obj_not_found(obj_id)
        session = db_session.create_session()
        obj = session.query(objects.Object).get(obj_id)
        return jsonify({"objects": obj.to_dict(
            only=('name', 'category', 'price', 'description', 'user_id', 'sold')
        )})

    def put(self):
        pass

    def post(self):
        pass

    def delete(self, obj_id):
        abort_if_obj_not_found(obj_id)
        session = db_session.create_session()
        obj = session.query(objects.Object).get(obj_id)
        session.delete(obj)
        session.commit()
        return jsonify({'success': 'OK'})


class ObjectsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        obj = session.query(objects.Object).all()
        return jsonify({"objects": [item.to_dict(
            only=('name', 'category', 'price', 'description', 'user_id', 'sold')
        ) for item in obj]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        proverka = session.query(users.User).filter(users.User.id == args['user_id']).first()
        if proverka is None:
            abort(404, message=f"Cant find user with id = {args['id']} :/")
        proverka = session.query(objects.Object).filter(objects.Object.id == args['id']).first()
        if proverka:
            abort(404, message=f"Object with id = {args['id']} already exists :/")
        obj = objects.Object()
        obj.id = args['id']
        obj.name = args['name']
        if args['category'] is None:
            args['category'] = 'Другое'
        obj.category = args['category']
        obj.price = args['price']
        obj.description = args['description']
        obj.user_id = args['user_id']
        obj.sold = args.get('sold', 0)
        obj.name_for_find = args['name']
        obj.pictures = ' '
        obj.block = 0
        obj.why_block = ' '
        session.add(obj)
        session.commit()
        return jsonify({'success': 'OK'})

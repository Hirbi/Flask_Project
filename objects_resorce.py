from flask_restful import Resource, abort, reqparse
from flask import jsonify
from data import db_session, objects


def abort_if_obj_not_found(obj_id):
    session = db_session.create_session()
    obj = session.query(objects.Object).get(obj_id)
    if not obj:
        abort(404, message=f"Ошибка 404 \n Объект {obj_id} не найден")


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('category', required=True)
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('price', required=True, type=int)
parser.add_argument('description', required=True)
parser.add_argument('sold', required=True)


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
        obj = objects.Object(
            name=args['name'],
            category=args['category'],
            price=args['price'],
            description=args['description'],
            user_id=args['user_id'],
            sold=args['sold'])
        session.add(obj)
        session.commit()
        return jsonify({'success': 'OK'})

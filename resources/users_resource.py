from flask_restful import Resource, abort, reqparse
from flask import jsonify
import datetime
from data import db_session, users


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    user = session.query(users.User).get(user_id)
    if not user:
        abort(404, message=f"User with id {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('phone', required=True, type=int)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('town', required=True)
parser.add_argument('admin_password')


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(users.User).get(user_id)
        return jsonify({"users": user.to_dict(
            only=('id', 'name', 'phone', 'email', 'created_date', 'block')
        )})

    def put(self):
        pass

    def post(self):
        pass

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(users.User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(users.User).all()
        return jsonify({"users": [item.to_dict(
            only=('id', 'name', 'phone', 'email', 'created_date', 'block')
        ) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        proverka = session.query(users.User).filter(users.User.id == args['id']).first()
        if proverka:
            abort(404, message=f"User with id = {args['id']} already exists :/")
        user = users.User()
        user.id = args['id']
        user.name = args['name']
        user.phone = args['phone']
        user.email = args['email']
        user.password = args['password']
        user.town = args['town']
        user.created_date = datetime.datetime.now()
        user.block = False
        if args.get('admin_password', '') == 'AvsS1Fa2a!_trade':
            user.admin = 1
        else:
            user.admin = 0
        user.rating = None
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

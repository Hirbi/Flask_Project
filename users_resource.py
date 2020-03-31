from flask_restful import Resource, abort, reqparse
from flask import jsonify
from data import db_session, users


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    user = session.query(users.User).get(user_id)
    if not user:
        abort(404, message=f"Users {user_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('name', required=True)
parser.add_argument('phone', required=True, type=int)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)
parser.add_argument('created_date', required=True)
parser.add_argument('block', required=True)



class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(users.User).get(user_id)
        return jsonify({"users": user.to_dict(
            only=('id', 'name', 'phone', 'email', 'password', 'created_date', 'block')
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
            only=('id', 'name', 'phone', 'email', 'password', 'created_date', 'block')
        ) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = users.User(
            id=args['id'],
            name=args['name'],
            phone=args['phone'],
            email=args['email'],
            password=args['password'],
            created_date=args['created_date'],
            block=args['block']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})

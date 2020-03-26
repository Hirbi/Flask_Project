import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Object(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'objects'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    pictures = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=' ')
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    sold = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=False)
    user = orm.relation('User')

    def __repr__(self):
        return f'|id:{self.id}, name:{self.name},' \
               f' desc:{self.description}, author:{self.user.name}, pics: {self.pictures}|'

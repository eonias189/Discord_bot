import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    score = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    last_complexity = sqlalchemy.Column(sqlalchemy.String)
    last_ans = sqlalchemy.Column(sqlalchemy.String)

    def __repr__(self):
        return f'<User name: {self.name}>'

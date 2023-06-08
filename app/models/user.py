from datetime import timedelta, datetime
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from app.models.base import Base


class User(UserMixin, Base):
    __tablename__ = 'user'

    fields = ['username', 'nickname', 'permission', 'status', 'roles']
    username = Column(String(100), primary_key=True)
    nickname = Column(String(100), nullable=True)
    password = Column(String(100), nullable=False)
    permission = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)

    def get_id(self):
        from authlib.jose import jwt
        key = current_app.config['SECRET_KEY']
        expire = datetime.now() + timedelta(days=current_app.config['EXPIRE_IN'])
        header = {'alg': 'HS256'}
        data = {'id': self.id, 'pwd': self.password, 'exp': expire}
        return str(jwt.encode(header=header, payload=data, key=key), encoding='utf-8')

    @property
    def id(self):
        return self.username

    @property
    def token(self):
        return self.get_id()

    @property
    def roles(self):
        if self.permission == 1:
            return ['admin']
        elif self.permission == 0:
            return ['editor']

    def check_password(self, password):
        return self.password == password

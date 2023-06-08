from datetime import timedelta, datetime
from .app import Flask
from flask_cors import CORS
from flask_login import LoginManager
from app.api.v1 import create_blueprint_v1
from app.libs.error_code import AuthFailed
from app.models.base import db
from app.models.user import User
from app.models.mapping import Mapping

cors = CORS(supports_credentials=True)
login_manager = LoginManager()


@login_manager.request_loader
def load_user(req):
    from authlib.jose import jwt
    from flask import current_app
    key = current_app.config['SECRET_KEY']
    expire = datetime.now()
    token = req.headers.get('Authorization')
    if token is None:
        token = req.args.get('token')
    if token:
        if not Mapping.get_by_id(token):
            raise AuthFailed("token is invalid")
        try:
            data = jwt.decode(token, key)
        except:
            raise AuthFailed("token is error")
        if data.get('exp') < expire.timestamp():
            Mapping.get_by_id(token).deleted()
            raise AuthFailed("token has expired")
        _id = data.get('id')
        pwd = data.get('pwd')
        user = User.get_by_id(_id)
        if not user.check_password(pwd):
            raise AuthFailed("token is invalid")
        return user
    raise AuthFailed


@login_manager.unauthorized_handler
def unauthorized_handler():
    return AuthFailed()


def register_blueprints(flask_app):
    flask_app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(flask_app):
    # 注册数据库
    db.init_app(flask_app)
    with flask_app.app_context():
        db.create_all()
    # 注册cors
    cors.init_app(flask_app)
    # 注册用户管理器
    login_manager.init_app(flask_app)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    register_blueprints(app)
    register_plugin(app)
    return app

from flask import jsonify, request
from flask_login import current_user, login_required
from app.libs.error_code import AuthFailed, DeleteSuccess, Success
from app.libs.redprint import RedPrint
from app.models.user import User
from app.validators.session import LoginForm
from app.models.mapping import Mapping
from app.libs.auth import admin_only
api = RedPrint('session')


@api.route("", methods=['GET'])
@login_required
def get():
    user = current_user
    user.fields = ['username', 'nickname', 'status', 'roles']
    return jsonify({
        'code': 0,
        'data': user
    })


@api.route("", methods=['POST'])
def create():
    form = LoginForm().validate_for_api().data_
    user = User.get_by_id(form['username'])
    if user is None:
        raise AuthFailed('User not found')
    if not user.check_password(form['password']):
        raise AuthFailed('Wrong username or password')
    Mapping.set_token(user.token)
    raise Success({
        "token" :  user.token
    })


@api.route("", methods=['DELETE'])
def delete():
    token = request.headers.get("Authorization")
    Mapping.delete_by_id(token)
    raise DeleteSuccess('Logout successful')

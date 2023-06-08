from flask import jsonify
from flask_login import current_user, login_required

from app.libs.auth import admin_only
from app.libs.error_code import CreateSuccess, Forbidden, NotFound, Success
from app.libs.redprint import RedPrint
from app.models.user import User
from app.validators.user import CreateUserForm, ModifyUserForm, SearchUserForm

api = RedPrint('user')


@api.route("/<string:id_>", methods=['GET'])
@login_required
def get(id_):
    user = User.get_by_id(id_)
    if user is None:
        raise NotFound('User not found')
    return jsonify({
        "code": 0,
        "data": user
    })


@api.route("", methods=['POST'])
def create():
    form = CreateUserForm().validate_for_api().data_
    form['nickname'] = form['username']
    form['permission'] = 0
    form['status'] = 1
    User.create(**form)
    raise CreateSuccess('User has been created')


@api.route("/<string:id_>", methods=['POST'])
@login_required
def modify(id_):
    form = ModifyUserForm().validate_for_api().data_
    if current_user.permission != 1:
        if current_user.id != id_:
            raise Forbidden()

    user = User.get_by_id(id_)
    if user is None:
        raise NotFound('User not found')
    if form['id']:
        raise Forbidden('id 不可修改')
    user.modify(**form)
    raise Success('User has been modified')


@api.route("", methods=['GET'])
@admin_only
def search():
    form = SearchUserForm().validate_for_api().data_
    res = User.search(**form)
    return jsonify({
        'code': 0,
        'data': res
    })

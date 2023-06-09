from flask import jsonify
from flask_login import current_user, login_required
from app.libs.enums import UserStatusEnum, UserPermissionEnum
from app.libs.error_code import DeleteSuccess, Forbidden, NotFound, Success
from app.libs.redprint import RedPrint
from app.models.user import User
from app.validators.user import CreateUserForm, ModifyUserForm, SearchUserForm

api = RedPrint('user')

# 获取个人资料
@api.route("", methods=['GET'])
@login_required
def get():
    user = User.get_by_id(current_user.id)
    if user is None:
        raise NotFound('User not found')
    return jsonify({
        "code": 0,
        "data": user
    })


# 注册
@api.route("", methods=['POST'])
def create():
    form = CreateUserForm().validate_for_api().data_
    form['nickname'] = form['username']
    form['permission'] = UserPermissionEnum.USER
    form['status'] = UserStatusEnum.ACTIVE
    User.create(**form)
    raise Success


# 修改个人资料
@api.route("", methods=['POST'])
@login_required
def modify_only_self():
    form = ModifyUserForm().validate_for_api().data_
    user = User.get_by_id(current_user.id)
    if user is None:
        raise NotFound('User not found')
    if form['username']:
        raise Forbidden('can not modify')
    user.modify(**form)
    raise Success


# 注销
@api.route("", methods=['DELETE'])
@login_required
def delete():
    user = User.get_by_id(current_user.id)
    if user.username == 'admin':
        raise Forbidden("super管理员账户禁止注销")
    user.delete()
    raise DeleteSuccess()

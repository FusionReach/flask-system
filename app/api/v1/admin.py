# -*- coding: utf-8 -*-
# @Time    : 2023/6/9 14:06 
# @File    : admin.py

from flask_login import current_user
from app.libs.auth import admin_only
from app.libs.error_code import Forbidden, NotFound, Success
from app.libs.redprint import RedPrint
from app.models.user import User
from app.validators.user import ModifyUserForm, SearchUserForm

api = RedPrint('admin')

@api.route("<string:id_>", methods=['POST'])
@admin_only
def modify(id_):
    form = ModifyUserForm().validate_for_api().data_
    user = User.get_by_id(id_)
    if user is None:
        raise NotFound('User not found')
    if form['username']:
        raise Forbidden('can not modify username')
    if user.permission == 1 and user.id != current_user.id:
        raise Forbidden('can not modify other admin user')
    user.modify(**form)
    raise Success

@api.route("", methods=['GET'])
@admin_only
def search():
    form = SearchUserForm().validate_for_api().data_
    User.fields.append("create_time")
    User.fields.hide("password")
    res = User.search(**form)
    raise Success(res)
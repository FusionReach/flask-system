from app.libs.error import APIException


# 暂时预留1000-1999为内部错误
# 2000之后为各模块错误使用
class Success(APIException):
    code = 201
    msg = 'ok'
    error_code = 0
    data = None

    def __init__(self, data=None):
        self.data = data
        super(Success, self).__init__(msg=self.msg, code=self.code,
                                      error_code=self.error_code, data=self.data)

class CreateSuccess(APIException):
    code = 201
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 1


class ServerError(APIException):
    code = 500
    msg = 'sorry, the mistake happened'
    error_code = 999


class ClientTypeError(APIException):
    # 400 401 403 404
    # 500
    # 200 201 204
    # 301 302
    code = 400
    msg = 'client is invalid'
    error_code = 1001

class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1002


class NotFound(APIException):
    code = 404
    msg = 'the resource are not found O__O...'
    error_code = 1003


class AuthFailed(APIException):
    code = 401
    error_code = 1004
    msg = 'authorization failed'


class Forbidden(APIException):
    code = 403
    error_code = 1005
    msg = 'forbidden, not in scope'


from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    error_code = 999
    data = None

    def __init__(self, msg=None, code=None, error_code=None, data=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIException, self).__init__(msg)

    def get_body(self, environ=None, scope=None):
        body = {
            'msg': self.msg,
            'code': self.error_code,
            'request': request.method + ' ' + self.get_url_no_param()
        }
        if self.data:
            body['data'] = self.data
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

    @property
    def to_dict(self):
        d = {
            'msg': self.msg,
            'code': self.error_code,
            'request': request.method + ' ' + self.get_url_no_param()
        }
        if self.data:
            d['data'] = self.data
        return d





from flask import Flask as _Flask
from datetime import datetime, date
from app.libs.error import APIException
from flask.json.provider import DefaultJSONProvider as _JSONProvider


class JSONProvider(_JSONProvider):
    def default(self, o):
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        elif hasattr(o, 'fields'):
            d = dict()
            for key in o['fields']:
                d[key] = o[key]
            return d
        elif isinstance(o, bytes):
            return str(o, encoding='utf8')
        elif isinstance(o, APIException):
            return o.to_dict
        elif isinstance(o, datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        else:
            return _JSONProvider.default(o)


class Flask(_Flask):
    json_provider_class = JSONProvider





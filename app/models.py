from marshmallow import Schema, fields, validate
import hashlib
from datetime import datetime

from .settings import Settings

settings = Settings()


class MessageSchema(Schema):
    count = fields.Integer(required=True)
    ip = fields.Str()
    datetime = fields.DateTime(missing=lambda: datetime.utcnow().isoformat())
    reply_to = fields.List(fields.Integer())
    ident = fields.Method('get_ident', dump_only=True)
    name = fields.Str()
    body = fields.Str()
    country = fields.Str()
    country_name = fields.Str()
    type = fields.Str(default='public', validate=validate.OneOf(['public', 'private']))

    def get_ident(self, obj):
        h = hashlib.sha256()
        h.update('{}{}'.format(settings.SALT, obj.get('ip', '127.0.0.1')).encode('UTF-8'))
        return h.hexdigest()

    def dump_message(self, obj):
        dump = self.dump(obj)
        return {'type': 'message', 'data': dump.data}

    class Meta:
        exclude = ('ip',)

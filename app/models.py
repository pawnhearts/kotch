from marshmallow import Schema, fields, validate, pre_load
import hashlib
from datetime import datetime

from .settings import settings


class FileSchema(Schema):
    file = fields.Str()
    thumb = fields.Str(required=False, allow_none=True)
    width = fields.Integer(required=False, allow_none=True)
    height = fields.Integer(required=False, allow_none=True)
    duration = fields.Str(required=False, allow_none=True)
    filename = fields.Str()
    size = fields.Integer()
    type = fields.Str(default='image', validate=validate.OneOf(['image', 'video', 'audio']))


class MessageSchema(Schema):
    count = fields.Integer(required=True)
    ip = fields.Str()
    datetime = fields.DateTime(missing=lambda: datetime.utcnow().isoformat())
    reply_to = fields.List(fields.Integer(), required=False)
    ident = fields.Method('get_ident', dump_only=True)
    name = fields.Str()
    body = fields.Str()
    country = fields.Str()
    country_name = fields.Str()
    file = fields.Nested(FileSchema(), required=False, allow_none=True)
    type = fields.Str(default='public', validate=validate.OneOf(['public', 'private']))

    def get_ident(self, obj):
        h = hashlib.sha256()
        h.update('{}{}'.format(settings.SALT, obj.get('ip', '127.0.0.1')).encode('UTF-8'))
        return h.hexdigest()

    def dump_message(self, obj):
        dump = self.dump(obj)
        return {'type': 'message', 'data': dump.data}

    @pre_load
    def split_reply_to(self, in_data):
        if 'reply_to' in in_data:
            in_data = dict(in_data)
            if isinstance(in_data['reply_to'], str):
                in_data['reply_to'] = in_data['reply_to'].split()
            if not in_data['reply_to']:
                del in_data['reply_to']
        return in_data

    class Meta:
        exclude = ('ip',)

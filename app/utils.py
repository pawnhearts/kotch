import hashlib
from .settings import settings


def get_ident(remote_ip):
    h = hashlib.sha256()
    h.update('{}{}'.format(settings.SALT, remote_ip).encode('UTF-8'))
    return h.hexdigest()

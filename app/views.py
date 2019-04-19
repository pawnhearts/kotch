from datetime import datetime
import json

import aiohttp
from aiohttp import web
from aiohttp.hdrs import METH_POST
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPFound
import asyncio
from uuid import uuid1

from .geoip import get_location
from .settings import BASE_DIR, settings
from .models import MessageSchema
from .thumbnails import make_thumbnail, get_extension


async def index(request):
    return web.FileResponse('templates/chat.html')


async def post(request):
    data = await request.post()
    file = data.get('file')
    fileobj = None
    schema = MessageSchema()
    data = schema.load(data).data

    if file:
        fileobj = {
            'file': '{}.{}'.format(uuid1(), get_extension(file.filename)),
            'filename': file.filename,
        }
        filepath = settings.uploads_path / fileobj['file']
        with open(filepath, 'wb') as f:
            f.write(file.file.read())
        fileobj['size'] = filepath.stat().st_size
        try:
            thumb = await make_thumbnail(settings.uploads_path / fileobj['file'])
            fileobj['thumb'], fileobj['width'], fileobj['height'], fileobj['duration'], fileobj['type'] = thumb
        except Exception as e:
            return web.json_response({'error': str(e)}, status=400)
    remote_ip = request.remote
    remote_ip ='217.23.3.171'
    message = schema.load({
        'count': request.app.messages[-1]['count']+1 if request.app.messages else 1,
        'body': data.get('body'),
        'name': data.get('name'),
        'icon': data.get('icon'),
        'file': fileobj,
        'location': get_location(remote_ip),
        'ip': remote_ip,
        'reply_to': data.get('reply_to'),
    })
    if message.errors:
        return web.json_response({'error': message.errors}, status=400)

    for client in request.app.clients:
        await client.send_json(schema.dump_message(message.data))
    request.app.messages.append(message.data)
    request.app.messages = request.app.messages[-10:]
    return web.json_response(schema.dump(message.data))


async def websocket(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    request.app.clients.add(ws)
    schema = MessageSchema()
    for message in request.app.messages:
        await ws.send_json(schema.dump_message(message))

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            print(data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    request.app.clients.remove(ws)
    return ws

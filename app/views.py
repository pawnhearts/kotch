from datetime import datetime
import json

import aiohttp
from aiohttp import web
import asyncio
from uuid import uuid1

from .utils import get_ident
from .geoip import get_location, get_location_from_country
from .settings import BASE_DIR, settings
from .models import MessageSchema
from .thumbnails import make_thumbnail, get_extension


async def index(request):
    return web.FileResponse('templates/chat.html')


async def post(request):
    postdata = dict(await request.post())
    file = postdata.pop('file') if 'file' in postdata else None
    if file:
        postdata['file'] = {'file': file.filename, 'filename': file.filename, 'size': 0}
    fileobj = None
    schema = MessageSchema()
    data = schema.load(postdata)
    if data.errors:
        return web.json_response({'error': data.errors}, status=400)
    data = data.data

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
            return web.json_response({'error': {'file': str(e)}}, status=400)

    remote_ip = request.remote
    remote_ip = '217.23.3.171'
    message = schema.load({
        'count': request.app.messages[-1]['count']+1 if request.app.messages else 1,
        'body': data.get('body'),
        'name': data.get('name'),
        'icon': data.get('icon'),
        'private_for': data.get('private_for'),
        'file': fileobj,
        'location': get_location(remote_ip) if 'country' not in postdata else get_location_from_country(postdata.get('country'), postdata.get('country_name')),
        'ip': remote_ip if 'ident' not in postdata else postdata['ident'],
        'reply_to': data.get('reply_to'),
        'type': 'public' if not data.get('private_for') else 'private',
    })
    message_json = schema.dump_message(message.data)

    if message.data['type'] == 'public':
        clients = request.app.clients
    else:
        clients = request.app.clients_by_ident.get(message.data['private_for'])
        clients = [clients] if clients is not None else []

    for client in clients:
        await client.send_json(message_json)

    request.app.messages.append(message.data)
    request.app.messages = request.app.messages[-10:]
    return web.json_response(message_json)


async def websocket(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ws.remote = request.remote
    ws.ident = get_ident(ws.remote)
    request.app.clients.add(ws)
    request.app.clients_by_ident[get_ident(request.remote)] = ws
    schema = MessageSchema()
    if not request.query.get('no_history'):
        for message in request.app.messages:
            if message['type'] == 'public' or message.get('private_for') == ws.ident:
                await ws.send_json(schema.dump_message(message))

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            print(data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    request.app.clients.remove(ws)
    request.app.clients_by_ident.pop(ws.ident)
    return ws

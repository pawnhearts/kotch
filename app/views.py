from datetime import datetime
import json

import aiohttp
from aiohttp import web
from aiohttp.hdrs import METH_POST
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPFound
import asyncio

from .main import BASE_DIR
from .models import MessageSchema


async def index(request):
    return web.FileResponse('templates/chat.html')


async def post(request):
    data = await request.post()
    schema = MessageSchema()
    data = schema.load(data).data
    name = data.get('name')
    body = data.get('body')
    file = data.get('file')
    if file:
        with open(BASE_DIR / 'static/uploads' / file.filename, 'wb') as f:
            f.write(file.file.read())

    message = {
        'count': request.app.messages[-1]['count']+1,
        'body': body,
        'name': name,
        'file': file and file.filename,
        'country': 'PL-77',
        'datetime': datetime.now()
    }
    for client in request.app.clients:
        await client.send_json(schema.dump_message(message))
    request.app.messages.append(message)
    request.app.messages = request.app.messages[-100:]
    return web.Response(text='ok')


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

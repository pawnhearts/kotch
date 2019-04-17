from datetime import datetime
import json

import aiohttp
from aiohttp import web
from aiohttp.hdrs import METH_POST
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPFound
import asyncio

from .models import MessageSchema


async def index(app, request):
    return web.FileResponse('templates/chat.html')


async def post(app, request):
    data = await request.post()
    schema = MessageSchema()
    data = schema.load(data)
    name = data.get('name')
    body = data.get('body')
    file = data.get('file')
    if file:
        with open('static/uploads/{}'.format(file.filename), 'wb') as f:
            f.write(file.file.read())

    message = {'body': body, 'name': name, 'file': file and file.filename, 'country': 'PL-77'}
    for client in clients:
        await client.send_json(schema.dump_message(message))
    app.messages.append(message)
    app.messages = app.messages[-100:]
    return web.Response(text='ok')


clients = set()


async def websocket(app, request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    schema = MessageSchema()
    for message in app.messages:
        await ws.send_json(schema.dump_message(message))

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            print(data)
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    clients.remove(ws)
    return ws

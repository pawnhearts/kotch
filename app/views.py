from datetime import datetime

import aiohttp
from aiohttp import web
from aiohttp.hdrs import METH_POST
from aiohttp.web import json_response
from aiohttp.web_exceptions import HTTPFound
import asyncio

import json


async def index(request):
    return web.FileResponse('templates/chat.html')


async def post(request):
    data = await request.post()
    name = data.get('name')
    body = data.get('body')
    print(clients)
    for client in clients:
        await client.send_json({'type': 'message', 'data': {'body': body, 'name': name, 'country': 'PL-77'}})
    return web.Response(text='ok')


clients = set()


async def websocket(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    await ws.send_json({'type': 'message', 'data': {'body': '11', 'country': 'RU-48'}})

    # WARNING: ws.__aiter__ is vulnerable to spam!
    # t. ncat Tue 16 Apr 2019 09:23:11 AM UTC
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            print(data)
            for client in clients:
                await client.send_json({'type': 'message', 'data': {'body': data['body'], 'country': 'RU-48', 'name': 'kot'}})
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')
    clients.remove(ws)
    return ws

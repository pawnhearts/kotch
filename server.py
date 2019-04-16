import aiohttp
from aiohttp import web
import logging
import json


async def index_handler(request):
    return web.FileResponse('templates/chat.html')
    return web.Response(body=open('templates/chat.html').read(), content_type="text/html")


async def post_handler(request):
    name = request.match_info.get('name', "Anonymous")
    body = request.match_info.get('body', "Anonymous")
    print(clients)
    for client in clients:
        logging.error(client)
        await client.send_json({'type': 'message', 'data': {'body': 'zz'}})
    return web.Response(text='ok')


clients = set()


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    await ws.send_json({'type': 'message', 'data': {'body': '11'}})

    # WARNING: ws.__aiter__ is vulnerable to spam!
    # t. ncat Tue 16 Apr 2019 09:23:11 AM UTC
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = json.loads(msg.data)
            print(data)
            for client in clients:
                await client.send_json({'type': 'message', 'data': {'body': data['body']}})
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')
    clients.remove(ws)
    return ws

app = web.Application()
app.add_routes([
    web.get('/', index_handler),
    web.post('/post', post_handler),
    web.get('/ws', websocket_handler)
])
app.router.add_static('/static/', path='static/', name='static')

web.run_app(app)

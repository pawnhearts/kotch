from pathlib import Path

from aiohttp import web

from .settings import Settings, BASE_DIR, THIS_DIR
from .views import index, post, websocket
from .tasks import start_background_tasks

# import uvloop
# uvloop.install()


def setup_routes(app):
    app.add_routes([
        web.get('/', index),
        web.post('/post', post),
        web.get('/ws', websocket),
    ])
    app.router.add_static('/static/', path=BASE_DIR / 'static/', name='static')


async def create_app():
    app = web.Application(client_max_size=40*1024*1024)
    settings = Settings()
    app.update(
        name='chat',
        settings=settings
    )
    app.messages = []
    app.clients = set()
    app.on_startup.append(start_background_tasks)

    setup_routes(app)
    return app

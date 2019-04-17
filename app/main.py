from pathlib import Path
from functools import partial

from aiohttp import web

from .settings import Settings
from .views import index, post, websocket


THIS_DIR = Path(__file__).parent
BASE_DIR = THIS_DIR.parent


def setup_routes(app):
    app.add_routes([
        web.get('/', partial(index, app)),
        web.post('/post', partial(post, app)),
        web.get('/ws', partial(websocket, app)),
    ])
    app.router.add_static('/static/', path='static/', name='static')


async def create_app():
    app = web.Application()
    settings = Settings()
    app.update(
        name='chat',
        settings=settings
    )
    app.messages = [
    ]

    setup_routes(app)
    return app

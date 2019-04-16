from pathlib import Path

from aiohttp import web

from .settings import Settings
from .views import index, post, websocket


THIS_DIR = Path(__file__).parent
BASE_DIR = THIS_DIR.parent


def setup_routes(app):
    app.add_routes([
        web.get('/', index),
        web.post('/post', post),
        web.get('/ws', websocket)
    ])
    app.router.add_static('/static/', path='static/', name='static')


async def create_app():
    app = web.Application()
    settings = Settings()
    app.update(
        name='chat',
        settings=settings
    )

    setup_routes(app)
    return app

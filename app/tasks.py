import asyncio
import pickle
import os

from .settings import Settings, BASE_DIR, THIS_DIR


def load_db(app):
    if (BASE_DIR /'messages.db').exists():
        with open(BASE_DIR /'messages.db', 'rb') as f:
            app.messages = pickle.load(f)


async def save_db(app):
    while True:
        await asyncio.sleep(5)
        with open(BASE_DIR /'messages.db', 'wb') as f:
            pickle.dump(app.messages, f)


async def start_background_tasks(app):
    # asyncio.get_child_watcher().attach_loop(app.loop)
    load_db(app)
    app['save_db_task'] = app.loop.create_task(save_db(app))

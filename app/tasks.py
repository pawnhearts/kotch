import asyncio
import pickle
import os


def load_db(app):
    if os.path.exists('messages.db'):
        with open('messages.db', 'rb') as f:
            app.messages = pickle.load(f)


async def save_db(app):
    while True:
        await asyncio.sleep(5)
        with open('messages.db', 'wb') as f:
            pickle.dump(app.messages, f)


async def start_background_tasks(app):
    load_db(app)
    app['save_db_task'] = app.loop.create_task(save_db(app))

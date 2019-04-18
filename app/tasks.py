import asyncio


async def save_db(app):
    while True:
        await asyncio.sleep(5)


async def start_background_tasks(app):
    app['save_db_task'] = app.loop.create_task(save_db(app))

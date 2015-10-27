import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(__file__)))

import time
import asyncio


import aiopg.sa
import sqlalchemy as sa
from motor.motor_asyncio import AsyncIOMotorClient

from aio_crud_store.aiopg_store import AiopgStore
from aio_crud_store.motor_store import MotorStore


DB_URI = 'postgresql:///aio_crud_store'

# create table
metadata = sa.MetaData()
metadata.bind = sa.create_engine(DB_URI)
table = sa.Table('aiopg_store', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('foo', sa.String()),
    sa.Column('spam', sa.Integer()),
)
metadata.drop_all()
metadata.create_all()


async def main():
    n = 1000

    print('\nMotor:')
    await motor_bench(n)

    print('Aiopg:')
    await aiopg_bench(n)


def timed(f):

    async def wrapper(*args, **kwargs):
        started = time.time()
        result = await f(*args, **kwargs)
        tooks = time.time() - started
        print('{} tooks {} seconds'.format(f.__name__, tooks))
        return result

    return wrapper


async def aiopg_bench(n):
    engine = await aiopg.sa.create_engine(DB_URI)
    store = AiopgStore(table, engine)
    await run_benchmarks(store, n)


async def motor_bench(n):
    db = AsyncIOMotorClient()['aio_crud_store']
    collection = db['motor_store']
    await collection.remove({})

    store = MotorStore(collection)
    await run_benchmarks(store, n)


async def run_benchmarks(store, n):
    ids = await create_bench(store, n)
    doc = await read_bench(store, ids)
    await update_bench(store, ids)


@timed
async def create_bench(store, n):
    ids = set()
    for i in range(n):
        id = await store.create({'foo': 'bar'})
        ids.add(id)
    return ids


@timed
async def read_bench(store, ids):
    for id in ids:
        await store.read(id=id)


@timed
async def update_bench(store, ids):
    for id in ids:
        await store.update(id, {'foo': 'baz'})


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

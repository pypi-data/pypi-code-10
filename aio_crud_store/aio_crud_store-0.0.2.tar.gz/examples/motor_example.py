import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(__file__)))

import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from aio_crud_store.motor_store import MotorStore


async def main():
    db = AsyncIOMotorClient()['aio_crud_store']
    collection = db['motor_store']
    await collection.remove({})

    # initialize store
    store = MotorStore(collection)

    # create
    id = await store.create({'foo': 'bar'})
    print(repr(id))  # ObjectId('...')

    # read
    doc = await store.read(foo='bar')
    print(doc)  # {'_id': ObjectId('...'), 'foo': 'bar'}

    # update
    await store.update(id, {'foo': 'baz', 'spam': 1})
    doc = await store.read(id=id)
    print(doc)  # {'_id': ObjectId('...'), 'foo': 'baz', 'spam': 1}

    # delete
    await store.delete(id)
    doc = await store.read(id=id)
    print(doc)  # None


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

import sys
from os.path import dirname
sys.path.insert(0, dirname(dirname(__file__)))

import asyncio

import aiopg.sa
import sqlalchemy as sa

from aio_crud_store.aiopg_store import AiopgStore


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
    engine = await aiopg.sa.create_engine(DB_URI)

    # initialize store
    store = AiopgStore(table, engine)

    # create
    id = await store.create({'foo': 'bar'})
    print(id)  # 1

    # read
    doc = await store.read(foo='bar')
    print(doc)  # {'id': 1, 'foo': 'bar', 'spam': None}

    # update
    await store.update(id, {'foo': 'baz', 'spam': 1})
    doc = await store.read(id=id)
    print(doc)  # {'id': 1, 'foo': 'baz', 'spam': 1}

    # delete
    await store.delete(id)
    doc = await store.read(id=id)
    print(doc)  # None


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

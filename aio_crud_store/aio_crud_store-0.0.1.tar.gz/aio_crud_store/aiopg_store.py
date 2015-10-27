# TODO: aiopg does not fully support async / await style yet:
# https://github.com/aio-libs/aiopg/issues/71

from asyncio import coroutine
from .base_store import BaseStore


class AiopgStore(BaseStore):

    def __init__(self, table, engine):
        self.table = table
        self.engine = engine

    @coroutine
    def create(self, data):
        query = self.table.insert().values(data)
        with (yield from self.engine) as conn:
            cursor = yield from conn.execute(query)
            id = (yield from cursor.first())[0]
        return id

    @coroutine
    def read(self, **filter):
        query = self.table.select()
        for k, v in filter.items():
            query = query.where(getattr(self.table.c, k) == v)
        with (yield from self.engine) as conn:
            cursor = yield from conn.execute(query.limit(1))
            row = yield from cursor.first()
        return row and dict(row)

    @coroutine
    def update(self, id, data):
        query = self.table.update().where(self.table.c.id == id).values(data)
        with (yield from self.engine) as conn:
            yield from conn.execute(query)

    @coroutine
    def delete(self, id):
        query = self.table.delete().where(self.table.c.id == id)
        with (yield from self.engine) as conn:
            yield from conn.execute(query)

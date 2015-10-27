from .base_store import BaseStore


class MotorStore(BaseStore):
    def __init__(self, collection):
        self.collection = collection

    def create(self, data):
        return self.collection.save(data)

    def read(self, **filter):
        query = {'_id' if k == 'id' else k: v for k, v in filter.items()}
        return self.collection.find_one(query)

    def update(self, id, data):
        return self.collection.update({'_id': id}, {'$set': data})

    async def delete(self, id):
        return await self.collection.remove({'_id': id})

class BaseStore:
    async def create(self, data):
        '''
        Save document and return it's id.
        '''
        raise NotImplementedError

    async def read(self, **filter):
        '''
        Return document by simple query or None.

        :Parameters:
            - `**filter`: a simple filter criteria like `id=1, active=True`
        '''
        raise NotImplementedError

    async def update(self, id, data):
        '''
        Update certain fields and return document.
        Removing of fields is not supported for compatibility with SQL
        databases.

        :Parameters:
            - `id`: id of document
            - `data`: dictionary of keys and values to update
        '''
        raise NotImplementedError

    async def delete(self, id):
        '''
        Remove document by it's id.
        '''
        raise NotImplementedError

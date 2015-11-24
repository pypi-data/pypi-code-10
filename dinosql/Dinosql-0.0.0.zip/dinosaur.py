# This package implements the DiNoSQL database.
class DiNoSQLClient:
    def __iter__(self, autocommit=False):
        self.autocommit = autocommit
        print('ROOOOOAR')

    def execute(self):
        print('HISSSSSSS')

    def commit(self):
        print('*Smashing things*')
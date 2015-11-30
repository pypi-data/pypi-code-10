from orator.migrations import Migration


class TestCreation(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('tests') as table:
            table.increments('id')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('tests')

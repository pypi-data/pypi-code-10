import json
from .constants import COLUMNS_MAPPER


class Provider(object):

    def __init__(self, data_file, options, *args, **kwargs):
        with open(data_file) as data:
            self.data = json.load(data)

        self.delimiter = options['delimiter']
        self.omit_columns = options['omit_columns']

        # Fields to output. This will output every fields by default
        self.fields = options['fields']

    @staticmethod
    def generate_cells_length(data, columns):
        """
        Return dict mapping column to max cell length for that column.
        For example: { "id": 20, "desc": 30 }
        """
        cells_length = {}
        for row in data:
            for column in columns:
                # No existing cells_length for column
                if column not in cells_length:
                    cells_length[column] = len(row[column])
                    continue

                # For given column, if current cell length is greater than existing cells_length
                if len(row[column]) > cells_length[column]:
                    cells_length[column] = len(row[column])

        return cells_length

    def render(self, data):
        cells_length = self.generate_cells_length(data, self.fields)
        for row in data:
            print (self.generate_row_output(row, self.fields, cells_length))

    def generate_row_output(self, row, columns, cells_length):
        output = ""
        for idx, column in enumerate(columns):
            # Column output
            if not self.omit_columns:
                output += COLUMNS_MAPPER[column] + ": "

            # Field output
            # To ensure evenly spaced cells we will add empty spaces to each cells until
            # it has the same length as the biggest cell for a given column
            output += row[column] + (cells_length[column] - len(row[column])) * " "

            # Delimiter output. don't output delimiter for last column
            if idx != (len(columns) - 1):
                output += self.delimiter
        return output

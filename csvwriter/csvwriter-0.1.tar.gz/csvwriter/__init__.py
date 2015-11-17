import csv
import itertools


class CsvWriter:
    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.rows = iter(())

    def append_row(self, new_row):
        self.append_rows([new_row])

    def append_rows(self, new_rows):
        self.rows = itertools.chain(self.rows, new_rows)

    def __lshift__(self, new_rows):
        if isinstance(new_rows, dict):
            self.append_row(new_rows)
        else:
            self.append_rows(new_rows)

    def flush(self):
        firstrow = next(self.rows)
        fieldnames = firstrow.keys()

        file_obj = self.csv_file.open('w') if hasattr(self.csv_file, 'open') else self.csv_file
        with file_obj as csv_f:
            writer = csv.DictWriter(csv_f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow(firstrow)
            writer.writerows(self.rows)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            return
        self.flush()

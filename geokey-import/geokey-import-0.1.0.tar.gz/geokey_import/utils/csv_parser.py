import csv


def get_fields(csv_file):
    reader = csv.DictReader(open(csv_file, 'rU'))
    return reader.fieldnames

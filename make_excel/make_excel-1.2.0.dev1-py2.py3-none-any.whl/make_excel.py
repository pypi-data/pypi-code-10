import os
import string
import random

from xlwt import easyxf
from xlwt import Workbook
from xlrd import open_workbook
from xlutils.copy import copy


def random_name_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))


def path_generator(size=5, chars=string.ascii_uppercase + string.digits):
    return os.getcwd() + '/' + 'output_' + random_name_generator(size, chars) + '.xls'


def make_excel(dict_data, full_filepath=None, sheet_name='Sheet1'):
    '''
        Example usage -> make_excel({'data': [1, 2, 3, 4, 5, 6, 7], 'data1': ['apples', 'oranges'],  'data3': 1}, full_filepath='output_NsURCM.xls')
    '''

    style = easyxf('font: bold 1; pattern: pattern solid, fore_colour gold;')
    if full_filepath:
        # use the provided path + name for excel
        if full_filepath.endswith('.xls'):
            full_filepath = full_filepath
        else:
            full_filepath = full_filepath + '.xls'
    else:
        # create a new path + name for excel
        full_filepath = path_generator()

    file_exists = os.path.isfile(full_filepath)
    # check if file already exist
    if file_exists:
        workbook = copy(open_workbook(full_filepath, formatting_info=True))
        sheet = workbook.add_sheet(sheet_name + random_name_generator(2))
    else:
        workbook = Workbook()
        sheet = workbook.add_sheet(sheet_name)

    for column, each_key in enumerate(dict_data.keys()):
        sheet.write(0, column, each_key, style)
        id_counter = 0
        if type(dict_data[each_key]) != list:
            for index, value in enumerate([dict_data[each_key]], start=1):
                sheet.write(index, column, value)
                id_counter = id_counter + 1
        else:
            for index, value in enumerate(dict_data[each_key], start=id_counter if id_counter else 1):
                sheet.write(index, column, value)

    workbook.save(full_filepath)

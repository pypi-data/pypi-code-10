from xlrd import open_workbook
import tempfile
import csv


class ExcelCsvReader():
    xlsx_sig = b'\x50\x4B\x05\06'
    xls_sig = b'\x09\x08\x10\x00\x00\x06\x05\x00'

    @classmethod
    def _is_xsl(cls, file_name):
            filenames = [
                (file_name, 0, 512, 8),
                (file_name, 2, -22, 4)]
            try:
                for filename, whence, offset, size in filenames:
                    with open(filename, 'rb') as f:
                        f.seek(offset, whence)  # Seek to the offset.
                        bytes = f.read(size)  # Capture the specified number of bytes.
                        if bytes == ExcelCsvReader.xls_sig:
                            return True
                        elif bytes == ExcelCsvReader.xlsx_sig:
                            return True
            except Exception as e:
                return False
            return False

    @classmethod
    def get_data(cls, file) -> dict:
        """
        get excel or csv file content
        
        :param file file: file from post body
        
        :raise: ExcelCsvReaderError
        :rtype: list of dict
        :return: file content
        """
        try:
            with tempfile.NamedTemporaryFile() as f:
                f.write(file.file.read())
                data = []
                f.seek(0)
                if cls._is_xsl(f.name):
                    f.seek(0)
                    book = open_workbook(f.name)
                    sheet = book.sheet_by_index(0)

                    # read header values into the list
                    keys = [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

                    for row_index in range(1, sheet.nrows):
                        d = {keys[col_index]: sheet.cell(row_index, col_index).value
                             for col_index in range(sheet.ncols)}
                        data.append(d)
                else:
                    data = [row for row in csv.DictReader(open(f.name))]

                return data

        except Exception:
            raise ExcelCsvReaderError('error while reading excel/csv file')


class ExcelCsvReaderError(Exception):
    pass
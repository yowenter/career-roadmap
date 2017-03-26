import xlsxwriter
import string


class ExcelDriver(object):
    def __init__(self, file_path=None, sheet_name=None, headers=None):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.headers = headers
        self._is_inited = False

    def write(self, item):
        self.current_index += 1
        for name, value in item.items():
            index = self.header_indexes[name]

            self.work_sheet.write('{}{}'.format(index, str(self.current_index)), value)

    def __enter__(self):
        if not self._is_inited:
            self.init()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.work_book.close()

    def init(self):
        self.work_book = xlsxwriter.Workbook(self.file_path)
        self.work_sheet = self.work_book.add_worksheet(self.sheet_name)
        self.header_indexes = dict(zip(self.headers, string.ascii_uppercase[:len(self.headers)]))
        for name, index in self.header_indexes.items():
            self.work_sheet.write('{}1'.format(index), name)

        self.current_index = 1

    def close(self):
        self.work_book.close()


if __name__ == '__main__':
    import os

    excel_file_path = os.path.join(os.getcwd(), 'test.xlsx')

    with ExcelDriver(excel_file_path, 'test', ['name', 'age']) as w:
        w.write({'name': 'haha', 'age': '18'})

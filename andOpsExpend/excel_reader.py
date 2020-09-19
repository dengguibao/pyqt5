import xlrd
import os


class ExcelReader:
    book_name = 'data.xls'
    sheet_name = 'Sheet1'
    wb = None
    tb = None

    def __init__(self, **kwargs):
        if kwargs['book_name']:
            self.book_name = kwargs['book_name']
        if kwargs['sheet_name']:
            self.sheet_name = kwargs['sheet_name']

    def get_data(self, field):
        """
        get specific field data from excel table
        :param field: list field list
        :return: data list
        """
        if not os.path.exists(self.book_name) or not field:
            return None

        self.wb = xlrd.open_workbook(self.book_name)
        self.tb = self.wb.sheet_by_name(self.sheet_name)
        cols = self.tb.ncols
        rows = self.tb.nrows
        data = []
        for r in range(1, rows):
            row_data = []
            for c in range(cols):
                if self.tb.cell(0, c).value in field:
                    cell_data = self.tb.cell(r, c).value
                    row_data.append(cell_data)
            if len(row_data) == len(field):
                data.append(row_data)
            del row_data
        if data:
            return data
        else:
            return None

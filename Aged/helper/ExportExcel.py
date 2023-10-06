import os
import pandas as pd

class DataFrameToExcel:
    def __init__(self, file_name):
        self.file_name = file_name
        self.check_and_create_file()

    def check_and_create_file(self):
        if not os.path.exists(self.file_name):
            df = pd.DataFrame()
            df.to_excel(self.file_name, index=False, engine='xlsxwriter')

    def append_data_to_excel(self, data_dict_list):
        df_data = pd.DataFrame(data_dict_list)
        writer = pd.ExcelWriter(self.file_name, engine='xlsxwriter')
        df_data.to_excel(writer, index=False)
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',  # Change the color here
            'border': 1
            })
        header_format.set_align('center')
        header_format.set_bold(True)
        for col_num, value in enumerate(df_data.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, len(value) * 2.5)
            worksheet.set_column(0, 0, 50)
        writer.close()
        print(f'Output saved to {self.file_name}')
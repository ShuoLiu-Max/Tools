import openpyxl
import xlrd

data = xlrd.open_workbook("openpyxl_file_0.xlsx")
table = data.sheets()[0]
table_val = table._cell_values


openpyxl_data = table_val
output_file_name = 'openpyxl_file_0.xlsx'
 
def save_excel(target_list, output_file_name):
    """
    将数据写入xlsx文件
    """
    if not output_file_name.endswith('.xlsx'):
        output_file_name += '.xlsx'
 
    # 创建一个workbook对象，而且会在workbook中至少创建一个表worksheet
    wb = openpyxl.Workbook()
    # 获取当前活跃的worksheet,默认就是第一个worksheet
    ws = wb.active
    title_data = ('a', 'b', 'c', 'd', 'e', 'f')
    target_list.insert(0, title_data)
    rows = len(target_list)
    lines = len(target_list[0])
    for i in range(rows):
        for j in range(lines):
            ws.cell(row=i + 1, column=j + 1).value = target_list[i][j]
 
    # 保存表格
    wb.save(filename=output_file_name)
 
 
save_excel(openpyxl_data, output_file_name)



pass
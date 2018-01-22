import parameters
import excel2shp as cur_tools

TestDataFolder = parameters.TestDataFolder
workData = parameters.workData
exceldata = TestDataFolder+workData
cur_tools.explore_workbook(exceldata)
attr_fields = cur_tools.create_fields_list(exceldata, currentSheet='glossary')

print(attr_fields)
print('Exporting data')
cur_tools.export_data_to_csv(exceldata,currentSheet='glossary')
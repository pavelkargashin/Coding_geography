# coding:utf-8
import parameters
import excel2shp as cur_tools

TestDataFolder = parameters.TestDataFolder
workData = parameters.workData
exceldata = TestDataFolder+workData
sheet_list = cur_tools.explore_workbook(exceldata)
data2process = cur_tools.choose_sheets(sheet_list)# список название тех листов, которые подходят для обработки
mydict = cur_tools.form_names(data2process)#В это словаре хранятся наименования для всех будущих шейпов
attr_fields = cur_tools.create_fields_list(exceldata, currentSheet=data2process[0])
shorten_field_names = cur_tools.shorten_field_name(attr_fields)
myshape = mydict[data2process[0]]+'.shp'
print('Exporting data')
tableDict = cur_tools.export_data_to_dictionary(exceldata,currentSheet=data2process[0], attr_names = shorten_field_names)
testData = tableDict[0:3]
cur_tools.create_shapefile(TestDataFolder+myshape, shorten_field_names, testData)

# coding:utf-8
import parameters
import Funcs_excel2shp as cur_tools

TestDataFolder = parameters.TestDataFolder
OutputFolder = parameters.TestDataFolder+'/Shapefiles/'
workData = parameters.workData
exceldata = TestDataFolder+workData

sheet_list = cur_tools.explore_workbook(exceldata)
data2process = cur_tools.choose_sheets(sheet_list)# список названий тех листов, которые подходят для обработки
mydict = cur_tools.form_names(data2process)#В этом словаре хранятся наименования для всех будущих шейпов
for item in data2process:
    attr_fields = cur_tools.create_fields_list(exceldata, currentSheet=item)
    shorten_field_names = cur_tools.shorten_field_name(attr_fields)
    myshape = str(mydict[item])+'.shp'
    print'Exporting data', str(myshape)
    tableDict = cur_tools.export_data_to_dictionary(exceldata,currentSheet=item, attr_names = shorten_field_names)
    testData = tableDict
    cur_tools.create_shapefile(OutputFolder+myshape, shorten_field_names, testData)

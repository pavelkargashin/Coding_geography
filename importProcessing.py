# coding:utf-8
import parameters
import Funcs_excel2shp as cur_tools
import ConvensionalCoordinates as coord

def main(exceldataFolder, excelName, keyword4search, OutputFolder):
    sheet_list = cur_tools.explore_workbook(exceldataFolder, excelName)
    data2process = cur_tools.choose_sheets(sheet_list, keyword4search)# список названий тех листов, которые подходят для обработки
    mydict = cur_tools.form_names(data2process)#В этом словаре хранятся наименования для всех будущих шейпов
    for item in data2process:
        attr_fields = cur_tools.create_fields_list(exceldataFolder+excelName, currentSheet=item)
        shorten_field_names = cur_tools.shorten_field_name(attr_fields)
        myshape = str(mydict[item])+'.shp'
        print 'Data export to: ', str(myshape)
        tableDict = cur_tools.export_data_to_dictionary(exceldataFolder+excelName, currentSheet=item, attr_names = shorten_field_names)
        testData = tableDict
        cur_tools.create_shapefile(OutputFolder+myshape, shorten_field_names, testData)

    print '\n#####################\nData has been imported\n#####################\n'
    coord.correct_coords(parameters.Sungai, parameters.Danau)

    print '\n#####################\nPointes were moved\n#####################\n'
if __name__ == "__main__":
    main()



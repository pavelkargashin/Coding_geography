# -*- coding:utf-8-*-

# Final Parameters

# PK work folder
ProjectFolder = 'C:/PAUL/Science/GISofBALI/ProjectFolder/'
# PK home folder
# ProjectFolder = ''

# AK work folder
# ProjectFolder = 'd:/YandexDisk/Projects/Bali/'

# Folders
InputData = ProjectFolder+"InputData/"
TempData = ProjectFolder+"TempData/"
OutputData = ProjectFolder+"OutputData/"
GISDataName = "GISEcologyBali"
ThematicDatasetName = 'ThematicData'
BasemapDatasetName = 'BasemapData'
AnalysisDatasetName = 'AnalysisData'

#Processing constants
excelName = 'StatData.xlsx'#название файла с тематическими данными
keyword4search = "Kualitas Air"# используется при выборе нужных листов в excel
Danau = 'AirDanau'
Sumur = 'AirSumur'
Sungai = 'AirSungai'
Laut = 'AirLaut'

#Dictionaries
#Accordance of sample type and field name in attribute table
field_dict = {Danau: 'LakeName',
              Sungai: 'RiverName',
              Sumur: 'Area',
              Laut: 'Point'}
#Accordance of sample type and field name in attribute table of polygon feature class
polyg_attr_name_dict = {Danau: 'Name',
                   Sungai: 'Basin'}
#Accordance of sample type and centroid feature class name
centroid_dict = {Danau: TempData+'/Lake_Center.shp',
                 Sungai: TempData+'/Basin_Center.shp'}
#Accordance of sample type and polygon feature class name
polyg_name_dict = {Danau: ProjectFolder+GISDataName+".gdb/"+BasemapDatasetName + '/Lakes',
                 Sungai: ProjectFolder+GISDataName+".gdb/"+BasemapDatasetName + '/Basins'}

fieldname = 'Year'#Параметр для разбивки данных по годам
fieldname_2 = 'Stage'#Параметр для разбивки данных по месяцам
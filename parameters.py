# -*- coding:utf-8-*-

# Final Parameters

# PK work folder
# ProjectFolder = 'C:/PAUL/Science/GISofBALI/ProjectFolder/'
# PK home folder
# ProjectFolder = ''

# AK work folder
ProjectFolder = 'd:/YandexDisk/Projects/Bali_Test/'

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
                        Sungai: 'Basin',
                        Sumur: 'Regency'}
#Accordance of sample type and centroid feature class name
centroid_dict = {Danau: TempData+'/Lake_Center.shp',
                 Sungai: TempData+'/Basin_Center.shp',
                 Sumur: TempData+'/Regency_Center.shp'}
#Accordance of sample type and polygon feature class name
polyg_name_dict = {Danau: ProjectFolder+GISDataName+".gdb/"+BasemapDatasetName + '/Lakes',
                   Sungai: ProjectFolder+GISDataName+".gdb/"+BasemapDatasetName + '/Basins',
                   Sumur: ProjectFolder+GISDataName+".gdb/"+BasemapDatasetName + '/Regency'}
#Accordance of sample type and last temathic field in attribute table
end_field = {Danau: "PO4_mgL",
             Sungai: "Cr_mgL",
             Sumur: "Turbidity_",
             Laut: "TotalColif"}
#Accordance of sample type and first temathic field in attribute table
first_field = {Danau: "DHL_mgL",
             Sungai: "TDS_mgL",
             Sumur: "TDS_mgL",
             Laut: "Color_CU"}
fieldname = 'Year' # Параметр для разбивки данных по годам
fieldname_2 = 'Stage' # Параметр для разбивки данных по месяцам

field_list_sungai = [u'TDS_mgL', u'TSS_mgL', u'DO_mgL', u'BOD_mgL', u'COD_mgL', u'NO2_N_mgL', u'NO3_N_mgL', u'NH3_N_mgL', u'FreeChlori', u'TotalP_mgL', u'Phenol_mgL', u'OilAndFat_', u'Detergent_', u'FecalColif', u'TotalColif', u'Cyanide_mg', u'Sulfide_mg', u'Turbidity_', u'Cd_mgL', u'Fe_mgL', u'PO4_mgL', u'SO4_mgL', u'Pb_mgL', u'Mn_mgL', u'Zn_mgL', u'Cr_mgL']
field_list_sumur = [u'Temperatur', u'TDS_mgL', u'TSS_mgL', u'pH', u'BOD_mgL', u'COD_mgL', u'DO_mgL', u'TotalP_mgL', u'NO3_N_mgL', u'NH3_N_mgL', u'As_mgL', u'Co_mgL', u'Ba_mgL', u'B_mgL', u'Se_mgL', u'Cd_mgL', u'Cr_V_mgLI', u'Cu_mgL', u'Fe_mgL', u'Pb_mgL', u'Mn_mgL', u'Hg_mgL', u'Zn_mgL', u'Chloride_m', u'Cyanide_mg', u'Fluoride_m', u'NO2_N_mgL', u'Sulphate_m', u'FreeChlori', u'Sulfide_mg', u'Salinity_m', u'FecalColif', u'TotalColif', u'Gloss_A_mg', u'Gloss_B_mg', u'DHL_mgL', u'Phenol_mgL', u'OilAndFat_', u'Detergent_', u'PO4_mgL', u'Turbidity_']

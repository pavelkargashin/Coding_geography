# /usr/bin
# -*-coding:utf-8-*-
import os
import sys
import shutil
import configparser

home = os.getenv("HOME")

# defs to create congigfile
def create_config(ProjectFolder, ConfigFileName):
    config = configparser.ConfigParser()
    config.add_section('Paths')
    config.set('Paths', 'ProjectFolder', ProjectFolder)
    config.set('Paths', 'InputData', ProjectFolder + "InputData/")
    config.set('Paths', 'TempData', ProjectFolder + "TempData/")
    config.set('Paths', 'OutputData', ProjectFolder + "OutputData/")
    config.set('Paths', 'GISDataName', "GISEcologyBali")
    config.set('Paths', 'Decoration', ProjectFolder + "Decoration/")
    config.set('Paths', 'ThematicDatasetName', 'ThematicData')
    config.set('Paths', 'BasemapDatasetName', 'BasemapData')
    config.set('Paths', 'AnalysisDatasetName', 'AnalysisData')
    config.set('Paths', 'mxdName', ProjectFolder+'GISEcologyBali.mxd')

    config.add_section('ImportParameters')
    config.set('ImportParameters', 'fieldname', 'Year')
    config.set('ImportParameters', 'fieldname_2', 'Stage')

    config.add_section('ProcessingConstants')
    config.set('ProcessingConstants', 'Danau', 'AirDanau')
    config.set('ProcessingConstants', 'Sumur', 'AirSumur')
    config.set('ProcessingConstants', 'Sungai', 'AirSungai')
    config.set('ProcessingConstants', 'Laut', 'AirLaut')

    config.add_section('Dictionaries')
    config.set('Dictionaries', 'field_dict_keys', "Danau,Sungai,Sumur,Laut")
    config.set('Dictionaries', 'field_dict_values', "LakeName,RiverName,Area,Point")
    config.set('Dictionaries', 'polyg_attr_name_dict_keys', "Danau,Sungai,Sumur")
    config.set('Dictionaries', 'polyg_attr_name_dict_values', "Name,Basin,Regency")
    config.set('Dictionaries', 'centroid_dict_keys', "Danau,Sungai,Sumur")
    config.set('Dictionaries', 'centroid_dict_values',"TempData+'/Lake_Center.shp',TempData+'/Basin_Center.shp',TempData+'/Regency_Center.shp'")
    config.set('Dictionaries', 'polyg_name_dict_keys', "Danau,Sungai,Sumur")
    config.set('Dictionaries', 'polyg_name_dict_values', "ProjectFolder+GISDataName+'.gdb/'+BasemapDatasetName+'/Lakes',ProjectFolder+GISDataName+'.gdb/'+BasemapDatasetName+'/Basins',ProjectFolder+GISDataName+'.gdb/'+BasemapDatasetName+'/Regency'")

    config.set('Dictionaries', 'end_field_keys', "Danau,Sungai,Sumur,Laut")
    config.set('Dictionaries', 'end_field_values', "PO4_mgL,Cr_mgL,Turbidity_,TotalColif")
    config.set('Dictionaries', 'first_field_keys', "Danau,Sungai,Sumur,Laut")
    config.set('Dictionaries', 'first_field_values', "DHL_mgL,TDS_mgL,TDS_mgL,Color_CU")

    config.add_section('FieldLists')
    config.set('FieldLists', 'field_list_sungai', "u'TDS_mgL',u'TSS_mgL',u'DO_mgL',u'BOD_mgL',u'COD_mgL',u'NO2_N_mgL',u'NO3_N_mgL',u'NH3_N_mgL',u'FreeChlori',u'TotalP_mgL',u'Phenol_mgL',u'OilAndFat_',u'Detergent_',u'FecalColif',u'TotalColif',u'Cyanide_mg',u'Sulfide_mg',u'Turbidity_',u'Cd_mgL',u'Fe_mgL',u'PO4_mgL',u'SO4_mgL',u'Pb_mgL',u'Mn_mgL',u'Zn_mgL',u'Cr_mgL'")
    config.set('FieldLists', 'field_list_sumur', "u'Temperatur',u'TDS_mgL',u'TSS_mgL',u'pH',u'BOD_mgL',u'COD_mgL',u'DO_mgL',u'TotalP_mgL',u'NO3_N_mgL',u'NH3_N_mgL',u'As_mgL',u'Co_mgL',u'Ba_mgL',u'B_mgL',u'Se_mgL',u'Cd_mgL',u'Cr_V_mgLI',u'Cu_mgL',u'Fe_mgL',u'Pb_mgL',u'Mn_mgL',u'Hg_mgL',u'Zn_mgL',u'Chloride_m',u'Cyanide_mg',u'Fluoride_m',u'NO2_N_mgL',u'Sulphate_m',u'FreeChlori',u'Sulfide_mg',u'Salinity_m',u'FecalColif',u'TotalColif',u'Gloss_A_mg',u'Gloss_B_mg',u'DHL_mgL',u'Phenol_mgL',u'OilAndFat_',u'Detergent_',u'PO4_mgL',u'Turbidity_'")

    with open(ProjectFolder + '/' + ConfigFileName, 'w') as config_file:
        config.write(config_file)


def update_filepath(inputpath):
    temppath = str(inputpath)
    outputpath = temppath.replace('\\', '/')
    return outputpath



configFile = 'CONFIGURATION.ini'
project_folder = update_filepath(sys.argv[1])
create_config(project_folder, configFile)
print(project_folder)
    


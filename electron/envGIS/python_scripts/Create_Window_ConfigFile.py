#!C:\Python27\ArcGIS10.5\python.exe
# -*-coding:utf-8-*-
import os
import sys
import shutil
import configparser
import arcpy
import General_Tools_ConfigFile as GTC
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

def move_config(path, file):
    config_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')+'/'+file
    shutil.move(path+'/'+file, config_path)
    return config_path

# создание папок по заданной в файле конфигурации структуре
def create_folders(inputpath):
    try:
       os.makedirs(inputpath)
       print "Folder {} has been created".format(inputpath)
    except OSError:
        if not os.path.isdir(inputpath):
            raise


def create_database(inputpath, GISName):
    if arcpy.Exists(inputpath+GISName+'.gdb/'):
       print "Geodatabase: ", inputpath+GISName+'.gdb/'
    else:

        arcpy.CreateFileGDB_management(inputpath, GISName)
        print "Geodatabase has been created: ", inputpath+GISName + '.gdb/'
    return inputpath+GISName + '.gdb'


def create_dataset(GDB,FDname):
    arcpy.env.workspace = GDB
    if arcpy.Exists(FDname):
        print "dataset {} exists".format(FDname)
    else:
        arcpy.CreateFeatureDataset_management(GDB, FDname, spatial_reference=arcpy.SpatialReference(4326))
        print 'dataset {} has been created'.format(FDname)


def create_project(configFileName):
    cur_section = 'Paths'
    ProjectFolder = GTC.get_setting(configFileName, cur_section, setting='projectfolder')
    InputData = GTC.get_setting(configFileName, cur_section, setting = 'inputdata')
    TempData = GTC.get_setting(configFileName, cur_section, setting = 'tempdata')
    OutputData = GTC.get_setting(configFileName, cur_section, setting = 'outputdata')
    DecorationFolder = GTC.get_setting(configFileName, cur_section, setting = 'decoration')
    GISName = GTC.get_setting(configFileName, cur_section, setting = 'gisdataname')
    BasemapDatasetName = GTC.get_setting(configFileName, cur_section, setting='basemapdatasetname')
    ThematicDatasetName = GTC.get_setting(configFileName, cur_section, setting='thematicdatasetname')
    AnalysisDatasetName = GTC.get_setting(configFileName, cur_section, setting='analysisdatasetname')
    mxdName = GTC.get_setting(configFileName, cur_section, setting='mxdname')

    create_folders(InputData)
    create_folders(TempData)
    create_folders(OutputData)
    create_folders(DecorationFolder)
    GDB = create_database(ProjectFolder, GISName)

    create_dataset(GDB, BasemapDatasetName)
    create_dataset(GDB, ThematicDatasetName)
    create_dataset(GDB, AnalysisDatasetName)
    print "\n#####################\nStorage has been created!\nYou can check it via Windows Explorer\n" \
          "#####################\nNow you should import data\n Please execute file - Create_Window_ImportData.py"




configFile = 'CONFIGURATION.ini'
project_folder = update_filepath(sys.argv[1])
create_config(project_folder, configFile)
config_path = move_config(project_folder, configFile)
create_project(config_path)
print(project_folder)

    


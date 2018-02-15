# -*-coding:utf-8-*-
import re
import configparser
import parameters_test
import arcpy
projectfolder = 'C:/PAUL/AAGISTesting/MYGIS/'
configFileName = 'CONFIGURATION.ini'
GIS = projectfolder+parameters_test.get_setting(projectfolder, configFileName, 'Paths', 'GISDataName')+'.gdb/'
ThematicDataset = GIS+parameters_test.get_setting(projectfolder, configFileName, 'Paths', 'ThematicDatasetName')+'/'
print GIS
print ThematicDataset
arcpy.env.workspace = ThematicDataset
listfc = arcpy.ListFeatureClasses()
print 'Total count of data '+ str(len(listfc)) + ' tables'


def create_stat(listfc):
    uniqEnv = set()
    uniqYear = set()
    uniqStage = set()
    for fc in listfc:
        result = re.split(r'_', fc)
        uniqEnv.add(result[0])
        uniqYear.add(result[1])
        uniqStage.add(result[2])
    return uniqEnv, uniqYear, uniqStage

def set_current_config(projectfolder, configFileName, listfc):
    config = configparser.ConfigParser()
    config.add_section("Existing Database")
    config.set("Existing Database", 'List_of_envs', str(create_stat(listfc)[0]))
    config.set("Existing Database", 'List_of_years', str(create_stat(listfc)[1]))
    config.set("Existing Database", 'List_of_stages', str(create_stat(listfc)[2]))

    with open(projectfolder+configFileName, 'a') as f:
        config.write(f)

set_current_config(projectfolder, configFileName, listfc)
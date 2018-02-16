# -*-coding:utf-8-*-
import re
import configparser
import arcpy

def create_listfc(ThematicDataset, criteria):
    arcpy.env.workspace = ThematicDataset
    listfc = arcpy.ListFeatureClasses(criteria)
    print 'Total count of data '+ str(len(listfc)) + ' tables'
    return listfc


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


# -*- coding:utf-8-*-
import os
import configparser


# Final Parameters

# Folders


def create_config(ProjectFolder, ConfigFileName):
    config = configparser.ConfigParser()
    config.add_section('Paths')
    config.set('Paths', 'ProjectFolder', ProjectFolder)
    config.set('Paths', 'InputData', ProjectFolder + "InputData/")
    config.set('Paths', 'TempData', ProjectFolder + "TempData/")
    config.set('Paths', 'OutputData', ProjectFolder + "OutputData/")
    config.set('Paths', 'GISDataName', "GISEcologyBali")
    config.set('Paths', 'ThematicDatasetName', 'ThematicData')
    config.set('Paths', 'BasemapDatasetName', 'BasemapData')
    config.set('Paths', 'AnalysisDatasetName', 'AnalysisData')

    config.add_section('ImportParameters')
    config.set('ImportParameters', 'fieldname', 'Year')
    config.set('ImportParameters', 'fieldname_2', 'Stage')

    with open(ProjectFolder+ConfigFileName, 'w') as config_file:
        config.write(config_file)


def get_config(path, ConfigFileName):
    if not os.path.exists(path + ConfigFileName):
        create_config(path,ConfigFileName)
    config = configparser.ConfigParser()
    config.read(path + ConfigFileName)
    return config


def get_setting(path, ConfigFileName, section, setting):
    config = get_config(path, ConfigFileName)
    value = config.get(section, setting)
    return value


def update_setting(path, ConfigFileName, section, setting, value):
    config = get_config(path, ConfigFileName)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)

def update_filepath(inputpath):
    temppath = str(inputpath)
    outputpath = temppath.replace('\\', '/')
    return outputpath






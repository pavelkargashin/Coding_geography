# -*- coding:utf-8-*-


import configparser, arcpy


def get_config(configFileName):
    config = configparser.ConfigParser()
    config.read(configFileName)
    return config


def get_setting(configFileName, section, setting):
    config = get_config(configFileName)
    value = config.get(section, setting)
    return value


def update_setting(configFileName, section, setting, value):
    config = get_config(configFileName)
    config.set(section, setting, value)
    with open(configFileName, "w") as config_file:
        config.write(config_file)


def update_filepath(inputpath):
    temppath = str(inputpath)
    outputpath = temppath.replace('\\', '/')
    return outputpath

def read_as_list(configFileName, section, setting):
    value = get_setting(configFileName, section, setting)
    return value.split(',')

def read_as_dict(configFileName, section, setting1, setting2):
    list_keys = read_as_list(configFileName, section, setting1)
    list_values = read_as_list(configFileName, section, setting2)
    return dict(zip(list_keys, list_values))




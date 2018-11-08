# -*- coding:utf-8-*-
import configparser


def get_config(configFileName):
    config = configparser.ConfigParser()
    config.read(configFileName)
    return config


def get_setting(configFileName, section, setting):
    config = get_config(configFileName)
    value = config.get(section, setting)
    return value


def update_setting(path, configFileName, section, setting, value):
    config = get_config(path, configFileName)
    config.set(section, setting, value)
    with open(path, "w") as config_file:
        config.write(config_file)


def update_filepath(inputpath):
    temppath = str(inputpath)
    outputpath = temppath.replace('\\', '/')
    return outputpath






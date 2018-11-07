# -*- coding:utf-8-*-
import configparser


def get_config(path, configFileName):
    config = configparser.ConfigParser()
    config.read(path + configFileName)
    return config


def get_setting(path, configFileName, section, setting):
    config = get_config(path, configFileName)
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






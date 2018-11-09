# -*-coding:utf-8 -*-
import os

import arcpy
import time
import General_Tools_ConfigFile as GTC


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

def create_mxd(ProjectFile):
    open(ProjectFile, 'w').close()
    os.startfile(ProjectFile)
    time.sleep(120)
    os.system("taskkill /f /im arcmap.exe")
    mxd = arcpy.mapping.MapDocument(ProjectFile)
    print mxd.dateSaved


def main(configFileName):


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
    create_mxd(mxdName)
    GDB = create_database(ProjectFolder, GISName)

    create_dataset(GDB, BasemapDatasetName)
    create_dataset(GDB, ThematicDatasetName)
    create_dataset(GDB, AnalysisDatasetName)
    print "\n#####################\nStorage has been created!\nYou can check it via Windows Explorer\n" \
          "#####################\nNow you should import data\n Please execute file - Create_Window_ImportData.py"

if __name__ == "__main__":
    main()

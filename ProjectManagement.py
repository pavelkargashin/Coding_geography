# -*-coding:utf-8 -*-
import os
import parameters
import parameters_test
import arcpy
configFileName = 'CONFIGURATION.ini'

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


def main():
    # Declare actual parameters
    ProjectFolder = parameters.ProjectFolder
    InputData = parameters.InputData
    TempData = parameters.TempData
    OutputData = parameters.OutputData
    GISName = parameters.GISDataName

    create_folders(ProjectFolder)
    create_folders(InputData)
    create_folders(TempData)
    create_folders(OutputData)
    GDB = create_database(ProjectFolder, GISName)

    create_dataset(GDB, parameters.BasemapDatasetName)
    create_dataset(GDB, parameters.ThematicDatasetName)
    create_dataset(GDB, parameters.AnalysisDatasetName)
    print "Storage has been created!\nYou can check it via Windows Explorer"



def main_2(ProjectFolder):
    create_folders(ProjectFolder)
    parameters_test.create_config(ProjectFolder, configFileName)

    section = 'Paths'
    InputData = parameters_test.get_setting(ProjectFolder, configFileName, section, setting = 'InputData')
    TempData = parameters_test.get_setting(ProjectFolder, configFileName, section, setting = 'TempData')
    OutputData = parameters_test.get_setting(ProjectFolder, configFileName, section, setting = 'OutputData')
    GISName = parameters_test.get_setting(ProjectFolder, configFileName, section, setting = 'GISDataName')
    BasemapDatasetName = parameters_test.get_setting(ProjectFolder, configFileName, section, setting='BasemapDatasetName')
    ThematicDatasetName = parameters_test.get_setting(ProjectFolder, configFileName, section, setting='ThematicDatasetName')
    AnalysisDatasetName = parameters_test.get_setting(ProjectFolder, configFileName, section, setting='AnalysisDatasetName')

    create_folders(InputData)
    create_folders(TempData)
    create_folders(OutputData)
    GDB = create_database(ProjectFolder, GISName)

    create_dataset(GDB, BasemapDatasetName)
    create_dataset(GDB, ThematicDatasetName)
    create_dataset(GDB, AnalysisDatasetName)
    print "\n#####################\nStorage has been created!\nYou can check it via Windows Explorer\n" \
          "#####################\nNow you should import data\n Please execute file - WindowImportData.py"

if __name__ == "__main__":
    main()

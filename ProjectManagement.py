# -*-coding:utf-8 -*-
import os
import parameters
import arcpy

# создание папок по заданной в файле parameters струкутре
def create_folders(inputpath):
    try:
       os.makedirs(inputpath)
       print "Папка {} создана".format(inputpath)
    except OSError:
        if not os.path.isdir(inputpath):
            raise


def create_database(inputpath, GISName):
    if arcpy.Exists(inputpath+GISName+'.gdb/'):
       print "База геоданных: ", inputpath+GISName+'.gdb/'
    else:

        arcpy.CreateFileGDB_management(inputpath, GISName)
        print "База геоданных создана: ", inputpath+GISName + '.gdb/'
    return inputpath+GISName + '.gdb'


def create_dataset(GDB,FDname):
    arcpy.env.workspace = GDB
    if arcpy.Exists(FDname):
        print "dataset {} уже существует".format(FDname)
    else:
        arcpy.CreateFeatureDataset_management(GDB, FDname, spatial_reference=arcpy.SpatialReference(4326))
        print 'dataset {} создан'.format(FDname)


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
    print "Структура хранения информации создана!"
    print "Самостоятельно скопируйте файл excel с данными в папку {}".format(InputData)

if __name__ == "__main__":
    main()

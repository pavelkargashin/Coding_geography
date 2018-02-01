# -*-coding:utf-8 -*-
import os
import parameters
import arcpy

# создание папок по заданной в файле parameters струкутре
def create_folders(inputpath):
    try:
       os.makedirs(inputpath)
       print "Папка для проекта создана"
    except OSError:
        if not os.path.isdir(inputpath):
            raise


def create_database(inputpath, GISName):
    if arcpy.Exists(inputpath+GISName+'.gdb/'):
       print "There is a GDB", inputpath+GISName+'.gdb/'
    else:
        print "Now we are creating GDB"
        arcpy.CreateFileGDB_management(inputpath, GISName)
        print "GDB was created", inputpath+GISName + '.gdb/'
    return inputpath+GISName + '.gdb'


def create_dataset(GDB,FDname):
    arcpy.env.workspace = GDB
    if arcpy.Exists(FDname):
        print "We have the sufficient dataset"
    else:
        arcpy.CreateFeatureDataset_management(GDB, FDname, spatial_reference=arcpy.SpatialReference(4326))
        print 'dataset {} was created'.format(FDname)



if __name__ == "__main__":
    # Declare actual parameters
    ProjectFolder = parameters.ProjectFolder
    InputData = parameters.InputData
    TempData = parameters.TempData
    GISName = parameters.GISDataName

    create_folders(ProjectFolder)
    create_folders(InputData)
    create_folders(TempData)
    GDB = create_database(ProjectFolder, GISName)

    create_dataset(GDB, parameters.BasemapDatasetName)
    create_dataset(GDB, parameters.ThematicDatasetName)
    print "The structure of our project was created"



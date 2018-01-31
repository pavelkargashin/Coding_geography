# -*- coding:utf-8-*-
import arcpy
import os
def set_database(PathToFolder, gisName, ThematicDatasetName):
    if os.path.exists(PathToFolder+gisName+'.gdb'):
        print "Our Database exists and it will be set as default!"
    else:
        arcpy.CreateFileGDB_management(PathToFolder, gisName)
        arcpy.CreateFeatureDataset_management(PathToFolder+gisName+'.gdb', ThematicDatasetName, spatial_reference= arcpy.SpatialReference(4326))

    currentGDB = PathToFolder + gisName + '.gdb'
    return currentGDB

def select_shapefiles(filepath):
    mylist = []
    alllist = os.listdir(filepath)
    for item in alllist:
        if item.endswith('.shp'):
            mylist.append(item)
        else:
            continue
    return mylist

# функция для составления списка feature classes в нужном dataset.
# возвращает список feature classes
def list_feature_classes(workspace):
    arcpy.env.workspace = workspace
    datalist = arcpy.ListFeatureClasses()
    return datalist

def extract_unique_values(fileToAnalize, fieldname):
    with arcpy.da.SearchCursor(fileToAnalize,[fieldname]) as cursor:
        return sorted({row[0] for row in cursor})

# Функция для разделения данных по году

def split_data_year(shapefile, datapath, fieldname):
    datalist = extract_unique_values(shapefile, fieldname)
    for datavalue in datalist:
        criteria = '{}={}'.format(fieldname, str(int(datavalue)))
        arcpy.Select_analysis(shapefile,datapath+'_'+str(int(datavalue)), criteria)

def split_data_stage(shapefile, datapath, fieldname):
    datalist = extract_unique_values(shapefile, fieldname)
    for datavalue in datalist:
        criteria = "{}='{}'".format(fieldname, str(datavalue))
        print criteria
        if datavalue == '99999999':
            arcpy.Select_analysis(shapefile, datapath + '_' + "NoStage", criteria)
        else:
            arcpy.Select_analysis(shapefile,datapath+'_'+str(datavalue), criteria)
# -*-coding:utf-8-*-
import arcpy
import os
import re
import parameters
import sys


def check_files(path2files, inputfiletype):
    list2load = []
    list2project = []
    inputfiles = os.listdir(path2files)
    for item in inputfiles:
        if item.endswith(inputfiletype) and re.search(r'Air', item)==None:
            print item
            desc = arcpy.Describe(path2files+item)
            spatReference = desc.spatialReference
            print spatReference.factoryCode
            if spatReference.factoryCode != destSpatRef:
                list2project.append(item)
            else:
                list2load.append(item)
        else:
            continue
    return list2load, list2project


def project_files(list2load, list2project):
    for item in list2project:
        outname = re.sub(inputfiletype,'',item)+postfix+inputfiletype
        arcpy.Project_management(inputFolder+item,inputFolder+outname,destSpatRef)
        list2load.append(outname)
    return list2load


def load_files(list2load):
    for item in list2load:
        outputname =re.sub(postfix,'',item)
        arcpy.FeatureClassToFeatureClass_conversion(inputFolder+item,outputFolder, re.sub(inputfiletype, '', outputname))
    return

if __name__ == "__main__":
    arcpy.env.overwriteOutput = True
    inputFolder = parameters.InputData
    inputfiletype = '.shp'
    outputFolder = parameters.ProjectFolder + parameters.GISDataName + '.gdb/' + parameters.BasemapDatasetName+'/'
    postfix = '_ProjectedFile'
    destSpatRef = 4326

    list2load, list2project = check_files(inputFolder, inputfiletype)

    loadings = project_files(list2load,list2project)
    print 'For data loads',loadings
    load_files(loadings)



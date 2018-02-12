# -*-coding:utf-8-*-
import arcpy
import os
import re
import parameters
import parameters_test
import sys
destSpatRef = 4326
inputfiletype = '.shp'
postfix = '_ProjectedFile'

def check_files(path2files, inputfiletype):
    list2load = []
    list2project = []
    inputfiles = os.listdir(path2files)
    for item in inputfiles:
        if item.endswith(inputfiletype) and re.search(r'Air', item)==None:
            desc = arcpy.Describe(path2files+item)
            spatReference = desc.spatialReference
            if spatReference.factoryCode != destSpatRef:
                list2project.append(item)
            else:
                list2load.append(item)
        else:
            continue
    return list2load, list2project


def project_files(inputFolder, list2load, list2project):
    for item in list2project:
        outname = re.sub(inputfiletype,'',item)+postfix+inputfiletype
        arcpy.Project_management(inputFolder+item,inputFolder+outname,destSpatRef)
        list2load.append(outname)
    return list2load


def load_files(inputFolder, list2load, outputFolder):
    for item in list2load:
        outputname =re.sub(postfix,'',item)
        arcpy.FeatureClassToFeatureClass_conversion(inputFolder+item,outputFolder, re.sub(inputfiletype, '', outputname))
    return


def main(ProjectFolder, ConfigurationFileName):
    arcpy.env.overwriteOutput = True
    inputFolder = parameters_test.get_setting(ProjectFolder, ConfigurationFileName,'Paths', 'InputData')
    outputFolder = ProjectFolder + parameters_test.get_setting(ProjectFolder, ConfigurationFileName,'Paths', 'GISDataName') + '.gdb/' + parameters_test.get_setting(ProjectFolder, ConfigurationFileName,'Paths', 'BasemapDatasetName') + '/'

    list2load, list2project = check_files(inputFolder, inputfiletype)
    loadings = project_files(inputFolder, list2load, list2project)
    load_files(inputFolder,loadings, outputFolder)
    print '\n#####################\nBaseMap imported\n#####################'


if __name__ == "__main__":
    main()



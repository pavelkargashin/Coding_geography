# -*-coding:utf-8-*-
import arcpy
import os
import re
import General_Tools_ConfigFile as GTC
destSpatRef = 4326
inputfiletype = '.shp'
projfiletype = '.prj'
postfix = '_ProjectedFile'
Paths = 'Paths'

def check_files(path2files, inputfiletype):
    list2load = []
    list2project = []
    inputfiles = os.listdir(path2files)
    for item in inputfiles:
        if item.endswith(inputfiletype) and re.search(r'Air', item)==None:
            item_prj = item.replace(inputfiletype, projfiletype)
            spatReference = arcpy.SpatialReference(path2files+item_prj)

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


def main(ConfigurationFileName):
    arcpy.env.overwriteOutput = True
    inputFolder = GTC.get_setting(ConfigurationFileName,Paths, 'inputdata')
    outputFolder = GTC.get_setting(ConfigurationFileName, Paths, 'projectfolder') + GTC.get_setting(ConfigurationFileName,Paths, 'gisdataname') + '.gdb/' + GTC.get_setting(ConfigurationFileName, Paths, 'basemapdatasetname') + '/'

    list2load, list2project = check_files(inputFolder, inputfiletype)
    loadings = project_files(inputFolder, list2load, list2project)
    load_files(inputFolder,loadings, outputFolder)
    print '\n#####################\nBaseMap imported\n#####################'


if __name__ == "__main__":
    main()



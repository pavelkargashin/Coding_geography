# -*- coding:utf-8-*-
import arcpy
import re

import databaseTools
import parameters
fieldname = parameters.fieldname
fieldname_2 = parameters.fieldname_2

inputfolder_shp = parameters.TempData
print "Check data and create database if it is critical"
envDatabase = parameters.ProjectFolder+parameters.GISDataName+'.gdb'
ThematicDataset = envDatabase + '/'+parameters.ThematicDatasetName
# Импорт в БГД и разделение по году
arcpy.RefreshCatalog(envDatabase)
arcpy.env.overwriteOutput = True
files2process = databaseTools.select_shapefiles(inputfolder_shp)
for item in files2process:
    print item
    newfilename = re.sub(r'\.shp','', item)
    print newfilename
    outputfile = ThematicDataset+'/'+newfilename
    databaseTools.split_data_year(inputfolder_shp+item,outputfile,fieldname)
print 'Import 1 has been finished'
# Разделение по этапу мониторинга
arcpy.RefreshCatalog(envDatabase)
fc2process = databaseTools.list_feature_classes(ThematicDataset)
for item in fc2process:
    databaseTools.split_data_stage(ThematicDataset+'/'+item, ThematicDataset+'/'+item, fieldname_2)


print 'Fin'


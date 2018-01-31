# -*- coding:utf-8-*-
import arcpy
import re

import databaseTools
import parameters
fieldname = 'Year'
fieldname_2 = 'Stage'

inputfolder_shp = parameters.TestDataFolder+'/Shapefiles/'
print "Check data and create database if it is critical"
envDatabase = databaseTools.set_database(parameters.PathToGIS, parameters.gisName, parameters.ThematicDataset)
# Импорт в БГД и разделение по году
arcpy.RefreshCatalog(envDatabase)
files2process = databaseTools.select_shapefiles(inputfolder_shp)
for item in files2process:
    print item
    newfilename = re.sub(r'\.shp','', item)
    print newfilename
    outputfile = envDatabase+'/'+parameters.ThematicDataset+'/'+newfilename
    databaseTools.split_data_year(inputfolder_shp+item,outputfile,fieldname)
print 'Import 1 has been finished'
# Разделение по этапу мониторинга
arcpy.RefreshCatalog(envDatabase)
fc2process = databaseTools.list_feature_classes(envDatabase+'/'+parameters.ThematicDataset)
for item in fc2process:
    databaseTools.split_data_stage(envDatabase+'/'+parameters.ThematicDataset+'/'+item, envDatabase+'/'+parameters.ThematicDataset+'/'+item, fieldname_2)


print 'Fin'


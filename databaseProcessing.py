# -*- coding:utf-8-*-
import arcpy
import re

import databaseTools
import parameters
fieldname = 'Year'

print "Check data and create database if it is critical"
envDatabase = databaseTools.set_database(parameters.PathToGIS, parameters.gisName, parameters.ThematicDataset)
files2process = databaseTools.select_shapefiles(parameters.TestDataFolder)
for item in files2process:
    print item
    newfilename = re.sub(r'\.shp','', item)
    print newfilename
    outputfile = envDatabase+'/'+parameters.ThematicDataset+'/'+newfilename
    databaseTools.split_data_year(parameters.TestDataFolder+item,outputfile,fieldname)

print 'Fin'


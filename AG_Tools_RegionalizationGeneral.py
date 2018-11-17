# coding: utf8
import arcpy, os, sys
import Maps_Tools_Regionalization
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

GISFolder = arcpy.GetParameterAsText(0)
regions = arcpy.GetParameterAsText(1)
env = arcpy.GetParameterAsText(2)
stats = arcpy.GetParameterAsText(3)
years = arcpy.GetParameterAsText(4)
indexes = arcpy.GetParameterAsText(5)

Maps_Tools_Regionalization.regionalisation_process(GISFolder=GISFolder, regions=str(regions), env=env, stats=stats, years=years, value_list=indexes)

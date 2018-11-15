# coding: utf8
import sys, arcpy, General_Tools_ConfigFile as GTC
import Maps_Tools_Regionalization
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

GISFolder = arcpy.GetParameterAsText(0)
regions = GTC.get_setting(config_file, Dictionaries, arcpy.GetParameterAsText(1))
env = arcpy.GetParameterAsText(2)
stats = arcpy.GetParameterAsText(3)
years = arcpy.GetParameterAsText(4)
indexes = arcpy.GetParameterAsText(5)

Regionalization.regionalisation_process(GISFolder, regions, env, stats, years, indexes)

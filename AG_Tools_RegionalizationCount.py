import arcpy
import Maps_Tools_Regionalization, General_Tools_ConfigFile as GTC

GISFolder = arcpy.GetParameterAsText(0)
env = arcpy.GetParameterAsText(1)
years = arcpy.GetParameterAsText(2)
indexes = arcpy.GetParameterAsText(3)

regions = GTC.get_setting(config_file, Dictionaries, env)
stats = "COUNT"
Regionalization.regionalisation_process(GISFolder, regions, env, stats, years, indexes)

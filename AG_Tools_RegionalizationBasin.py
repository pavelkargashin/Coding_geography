import arcpy
import Maps_Tools_Regionalization, General_Tools_ConfigFile as GTC

GISFolder = arcpy.GetParameterAsText(0)
env = arcpy.GetParameterAsText(1)
stats = arcpy.GetParameterAsText(2)
years = arcpy.GetParameterAsText(3)
indexes = arcpy.GetParameterAsText(4)
arcpy.AddMessage(indexes)
regions = GTC.get_setting(config_file, Dictionaries, 'Sungai')

Regionalization.regionalisation_process(GISFolder, regions, env, stats, years, indexes)

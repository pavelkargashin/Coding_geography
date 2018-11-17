import arcpy, os
import Maps_Tools_Regionalization, General_Tools_ConfigFile as GTC
config_file = os.getcwd()+ '/'+"CONFIGURATION"

GISFolder = arcpy.GetParameterAsText(0)
env = arcpy.GetParameterAsText(1)
stats = arcpy.GetParameterAsText(2)
years = arcpy.GetParameterAsText(3)
indexes = arcpy.GetParameterAsText(4)

dictionary = GTC.read_as_dict(config_file, "Dictionaries", "polyg_attr_name_dict_keys", "polyg_attr_name_dict_values")
regions = dictionary["Sumur"]

Maps_Tools_Regionalization.regionalisation_process(GISFolder=GISFolder, regions=str(regions), env=env, stats=stats, years=years, value_list=indexes)

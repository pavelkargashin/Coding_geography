import arcpy, os
import Maps_Tools_Regionalization, General_Tools_ConfigFile as GTC
config_file = os.getcwd()+ '/'+"CONFIGURATION"
project_folder = GTC.get_setting(config_file, "Paths", "projectfolder")

GISFolder = arcpy.GetParameterAsText(0)
env = arcpy.GetParameterAsText(1)
years = arcpy.GetParameterAsText(2)
indexes = arcpy.GetParameterAsText(3)

dictionary = GTC.read_as_dict(config_file, "Dictionaries", "polyg_attr_name_dict_keys", "polyg_attr_name_dict_values")
regions = dictionary["Sungai"]
stats = "COUNT"
Maps_Tools_Regionalization.regionalisation_process(GISFolder=GISFolder, regions=str(regions) + "s", env=env, stats=stats, years=years, value_list=indexes)

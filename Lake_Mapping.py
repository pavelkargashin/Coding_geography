import sys, arcpy, os, parameters, re, ConvensionalCoordinates, Regionalization, databaseTools
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

centroids = ConvensionalCoordinates.create_centroid(parameters.Danau)
lake_centroids = arcpy.FeatureClassToFeatureClass_conversion(in_features="D:/YandexDisk/Projects/Bali/TempData/Lake_Center.shp", out_path="D:/YandexDisk/Projects/Bali/GISEcologyBali.gdb", out_name="Lake_Centroids")
samples = parameters.Danau+".shp"
field_names = [f.name for f in arcpy.ListFields(samples)]
print field_names[10:]
years_list = databaseTools.extract_unique_values(samples, "Year")
print years_list
for field in field_names[10:]:
    for year in years_list:
        new_field = str(field) + "_" + str(int(year))
        new_field_list = []
        new_field_list.append(new_field)
        arcpy.AddField_management(lake_centroids, new_field, "FLOAT")

stats = "MAX"
text = Regionalization.dissolving_fields(field_names[10:], stats)
samples_dissolve = arcpy.Dissolve_management(samples, "D:/YandexDisk/Projects/Bali/GISEcologyBali.gdb/Danau_Dissolve",
                                             "LakeName;Year", text, "MULTI_PART")
# rows = arcpy.da.SearchCursor(samples_dissolve, ["Year", "LakeName", "MEAN_TDS_mgL"])
# value_list = []
# for row in rows:
#     value_list.append(row[2])
# del row
# del rows
# print value_list
lakes_list = databaseTools.extract_unique_values(samples_dissolve, "LakeName")
print lakes_list

field_list = field_names[10:]
for year in years_list:
    print year
    print years_list
    for lake in lakes_list:
        print lake
        print lakes_list
        for field in field_list:
            print field
            print field_list
            print stats+"_"+field
            print str(int(year))
            print lake
            rows = arcpy.da.SearchCursor(samples_dissolve, ["Year", "lakeName", stats+"_"+field])
            for row in rows:
                x = row[2]
                rows_update = arcpy.da.UpdateCursor(lake_centroids, ["Name", field+"_"+str(int(year))])
                for value in rows_update:
                    if value[0] == lake:
                        value[1] = x
                    rows_update.updateRow(value)
                del value
                del rows_update
            del row
            del rows






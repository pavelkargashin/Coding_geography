import sys, arcpy, os, parameters, re, ConvensionalCoordinates, Regionalization, databaseTools
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

lakes = "D:\\YandexDisk\\Projects\\Bali\\GISEcologyBali.gdb\\BasemapData\\Lakes"
lake_centroids = "D:/YandexDisk/Projects/Bali/GISEcologyBali.gdb/Lake_Centroids"
arcpy.FeatureToPoint_management(lakes, lake_centroids, "INSIDE")
samples_shp = parameters.Danau+".shp"
samples = arcpy.FeatureClassToFeatureClass_conversion(samples_shp,
                                                      "D:/YandexDisk/Projects/Bali/GISEcologyBali.gdb", "Danau")
years_list = databaseTools.extract_unique_values(samples, "Year")
field_names = Regionalization.update_fields(samples, 10)
for field in field_names[10:-1]:
    for year in years_list:
        new_field = str(field) + "_" + str(int(year))
        new_field_list = []
        new_field_list.append(new_field)
        arcpy.AddField_management(lake_centroids, new_field, "FLOAT")

stats = "MAX"
text = Regionalization.dissolving_fields(field_names[10:], stats)
samples_dissolve = arcpy.Dissolve_management(samples, "D:/YandexDisk/Projects/Bali/GISEcologyBali.gdb/Danau_Dissolve",
                                             "LakeName;Year", text, "MULTI_PART")
lakes_list = databaseTools.extract_unique_values(samples_dissolve, "LakeName")

field_list = field_names[10:-1]
for year in years_list:
    print year
    for lake in lakes_list:
        print lake
        for field in field_list:
            print stats+"_"+field
            rows = arcpy.da.SearchCursor(samples_dissolve, ["Year", "lakeName", stats+"_"+field])
            for row in rows:
                if row[0] == int(year) and row[1] == lake:
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






import sys, arcpy, parameters, Regionalization, databaseTools
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.workspace = parameters.ProjectFolder + parameters.GISDataName + ".gdb"
arcpy.env.overwriteOutput=True

# Calculation of total N
def NTotal_calculation(samples):
    arcpy.AddField_management(samples, "NTotal", "FLOAT")
    rows = arcpy.da.UpdateCursor(samples, ["NO2_mgL", "NO3_mgL", "NH3_mgL", "NTotal"])
    for row in rows:
        if row[0] and row[1] and row[2] is not None:
            row[3] = row[0] + row[1] + row[2]
        rows.updateRow(row)
    del row
    del rows
    return "NTotal"


lakes = parameters.polyg_name_dict[parameters.Danau]
lake_centroids = parameters.AnalysisDatasetName + "/Lake_Centroids"
arcpy.FeatureToPoint_management(lakes, lake_centroids, "INSIDE")
samples_shp = parameters.TempData + parameters.Danau+".shp"
samples = arcpy.FeatureClassToFeatureClass_conversion(samples_shp, arcpy.env.workspace, "Danau")
# Creating of table structure in a new feature class
years_list = databaseTools.extract_unique_values(samples, "Year")
field_names = Regionalization.update_fields(samples, 11)
field_names.append(NTotal_calculation(samples))
for field in field_names:
    for year in years_list:
        new_field = str(field) + "_" + str(int(year))
        new_field_list = []
        new_field_list.append(new_field)
        arcpy.AddField_management(lake_centroids, new_field, "FLOAT")
# Calculating of values for parameters, lakes and years
stats = "MAX" # Statistics type as parameter
text = Regionalization.dissolving_fields(field_names, stats)
output_dissolve = arcpy.env.workspace + "/" + parameters.AnalysisDatasetName + "/Danau_Dissolve"
samples_dissolve = arcpy.Dissolve_management(samples, output_dissolve, "LakeName;Year", text, "MULTI_PART")
lakes_list = databaseTools.extract_unique_values(samples_dissolve, "LakeName")
# Transposing values in attribute table
for year in years_list:
    print year
    for lake in lakes_list:
        print lake
        for field in field_names:
            rows = arcpy.da.SearchCursor(samples_dissolve, ["Year", "lakeName", stats+"_"+field])
            for row in rows:
                if row[0] == int(year) and row[1] == lake:
                    x = row[2]
                    rows_update = arcpy.da.UpdateCursor(lake_centroids, ["Name", field+"_"+str(int(year))])
                    for value in rows_update:
                        if value[0] == lake:
                            if x is not None:
                                value[1] = x
                            else:
                                value[1] = 0
                            rows_update.updateRow(value)
                    del value
                    del rows_update
            del row
            del rows

# Replacing Null values with zero
for field in [f.name for f in arcpy.ListFields(lake_centroids)]:
    rows = arcpy.da.UpdateCursor(lake_centroids, [field])
    for row in rows:
        if row[0] is None:
            row[0] = 0
        rows.updateRow(row)
    del row
    del rows
# Deleting temporal feature classes
delete_list = [samples, samples_dissolve]
for item in delete_list:
    arcpy.Delete_management(item)






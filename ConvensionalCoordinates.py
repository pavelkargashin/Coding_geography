# -*-coding:utf-8 -*-
import sys, arcpy, re
import parameters
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True


def move_point(dataFolder, dataType):
    inputData=dataFolder+dataType+'.shp'
    rows = arcpy.da.UpdateCursor(inputData, ["SHAPE@X", "SHAPE@Y", "KoordinatL", "NameLocati"])
    for row in rows:
        if row[2] == "99999999":
            Location = row[3]
            rows2 = arcpy.da.SearchCursor(inputData, ["SHAPE@X", "SHAPE@Y", "KoordinatL", "NameLocati"])
            for row2 in rows2:
                if row2[2] != "99999999" and row2[3] == Location:
                    X = row2[0]
                    Y = row2[1]
            del row2
            del rows2
            row[0] = X
            row[1] = Y
        rows.updateRow(row)
    del row
    del rows


def alter_name(samples, fieldlist, fieldnumber):
    rows = arcpy.da.UpdateCursor(samples, fieldlist)
    for row in rows:
        row[fieldnumber] = re.sub(r'Tukad\s', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'Tukad', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'TK', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'Tk', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\d', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\s+', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\(', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\)', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'BilukPoh', 'Bilukpoh', row[fieldnumber])
        row[fieldnumber] = re.sub(r's\.musiman', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r's\.musima', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r's\.mus', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'YehPenet', 'Penet', row[fieldnumber])
        row[fieldnumber] = re.sub(r'YehEmpas', 'Empas', row[fieldnumber])
        row[fieldnumber] = re.sub(r'yeh', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'Danau', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'Bendungan', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'Wos', 'Oos', row[fieldnumber])
        rows.updateRow(row)
    del row
    del rows
    return


def fill_missed_names(samples, fieldlist):
    rows = arcpy.da.UpdateCursor(samples, fieldlist)
    for row in rows:
        if row[2] == "99999999":
            if row[0] == " ":
                row[0] = row[1]
        rows.updateRow(row)
    del row
    del rows
    return


def move_data2polygon(sample_type):
    arcpy.JoinField_management(sample_type+'.shp', parameters.field_dict[sample_type],
                               parameters.centroid_dict[sample_type], parameters.polyg_attr_name_dict[sample_type])
    # Переместим непривязанные точки в координаты центроидов соответствующих бассейнов
    cursor = arcpy.da.UpdateCursor(sample_type+'.shp', ["SHAPE@X", "SHAPE@Y", "POINT_X", "POINT_Y", "KoordinatL"])
    for row in cursor:
        if row[4] == "99999999" and row[2] is not None:
            row[0] = row[2]
            row[1] = row[3]
        cursor.updateRow(row)
    del row
    del cursor
    return


def create_centroid(sample_type):
    alter_name(parameters.polyg_name_dict[sample_type], parameters.polyg_attr_name_dict[sample_type], 0)
    arcpy.FeatureToPoint_management(parameters.polyg_name_dict[sample_type], parameters.centroid_dict[sample_type],
                                    "INSIDE")
    arcpy.AddXY_management(parameters.centroid_dict[sample_type])
    return


sample_list = [parameters.Sungai, parameters.Danau]
for sample in sample_list:
    fieldlist = [parameters.field_dict[sample], "NameLocati", "KoordinatL"]
    dataFolder = parameters.TempData
    GISData = parameters.polyg_name_dict[sample]
    sample_type = sample + ".shp"
    fields = [0, 1]
    arcpy.RefreshCatalog(parameters.TempData)
    fill_missed_names(dataFolder + sample_type, fieldlist)
    for x in fields:
        alter_name(dataFolder + sample_type, fieldlist, x)
    create_centroid(sample)
    arcpy.env.workspace = dataFolder
    move_data2polygon(sample)
    delete_fields_list = arcpy.ListFields(sample_type)
    for field in delete_fields_list[-6:]:
        arcpy.DeleteField_management(sample_type,field.name)

# Проверка на неправильно привязанные точки
basins = parameters.polyg_name_dict[parameters.Sungai]
samples_identity = arcpy.Identity_analysis(dataFolder + parameters.Sungai + ".shp", basins, "Samples_Identity")
rows = arcpy.da.UpdateCursor(samples_identity, ["RiverName", "Basin", "Doubt"])
for row in rows:
    if row[2] == 1:
        if row[0] != row[1]:
            rows.deleteRow()
del row
del rows
arcpy.FeatureClassToFeatureClass_conversion(samples_identity, parameters.TempData, parameters.Sungai + ".shp")
arcpy.DeleteField_management(parameters.Sungai + ".shp","FID_AirSun")


arcpy.Delete_management(parameters.centroid_dict[parameters.Danau])
arcpy.Delete_management(parameters.centroid_dict[parameters.Sungai])
arcpy.Delete_management(samples_identity)
move_point(dataFolder, parameters.Danau)
move_point(dataFolder, parameters.Laut)



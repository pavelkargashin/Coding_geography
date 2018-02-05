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
            print Location
            for row2 in rows2:
                if row2[2] != "99999999" and row2[3] == Location:
                    X = row2[0]
                    Y = row2[1]
                    print X
                    print Y
            del row2
            del rows2
            row[0] = X
            row[1] = Y
        rows.updateRow(row)
    del row
    del rows


def change_basin_name(feature_class, fieldlist, fieldnumber):
    rows = arcpy.da.UpdateCursor(feature_class, fieldlist)
    for row in rows:
        row[fieldnumber] = re.sub(r'Tukad\s', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'Tukad', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'TK', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'Tk', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\d', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\s+', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'BilukPoh', 'Bilukpoh', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\(s\. musiman\)', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'YehPenet', 'Penet', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\(s\. musima', '', row[fieldnumber])
        row[fieldnumber] = re.sub(r'\(s\. mus', '', row[fieldnumber])
        rows.updateRow(row)
    del row
    del rows
    return

def fill_missed_names(feature_class, fieldlist):
    rows = arcpy.da.UpdateCursor(feature_class, fieldlist)
    for row in rows:
        if row[2] == "99999999":
            if row[0] == " ":
                row[0] = row[1]
        rows.updateRow(row)

def move_data2basin(feature_class, basin_data ):
    arcpy.JoinField_management(feature_class, "RiverName", basin_data, "Basin")
    # Переместим непривязанные точки в координаты центроидов соответствующих бассейнов
    cursor = arcpy.da.UpdateCursor(feature_class, ["SHAPE@X", "SHAPE@Y", "POINT_X", "POINT_Y", "KoordinatL"])
    for row in cursor:
        if row[4] == "99999999" and row[2] is not None:
            row[0] = row[2]
            row[1] = row[3]
        cursor.updateRow(row)
    del row
    del cursor


fieldlist = ["RiverName", "NameLocati", "KoordinatL"]
dataFolder = parameters.TempData
GISData = parameters.ProjectFolder+parameters.GISDataName+'.gdb/'+parameters.BasemapDatasetName+'/BasinsPolygon'
dataType = "AirSungai.shp"
fields = [0,1]
basin_data = dataFolder+'basinTemp.shp'


fill_missed_names(dataFolder+dataType, fieldlist)
for x in fields:
    change_basin_name(dataFolder+dataType,fieldlist, x)

arcpy.FeatureToPoint_management(GISData, basin_data, "INSIDE")
change_basin_name(basin_data,["Basin"], 0)
arcpy.AddXY_management(basin_data)

move_data2basin(dataFolder+dataType, basin_data)
river_fields_list = arcpy.ListFields(dataFolder+dataType)

for field in river_fields_list[-6:]:
    arcpy.DeleteField_management(dataFolder+dataType,field.name)



# move_point(dataFolder, parameters.Danau)
# move_point(dataFolder, parameters.Laut)



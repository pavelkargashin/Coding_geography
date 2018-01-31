# coding: utf8
import sys, arcpy, re, openpyxl
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

arcpy.env.workspace = "D:/YandexDisk/Projects/Bali/Bali.gdb"
input = "AirSungai"
input_samples = arcpy.Copy_management(input, "AirSungai_Copy")
input_basins = "Basins_FeatureToPoint"
def basin_name(feature_class, fieldnumber):
    rows = arcpy.da.UpdateCursor(feature_class, ["RiverName", "NameLocati", "KoordinatL"])
    for row in rows:
        if row[2] == "99999999":
            row[fieldnumber] = re.sub(r'Tukad\s', '', row[fieldnumber])
            row[fieldnumber] = re.sub(r'Tukad', '', row[fieldnumber])
            row[fieldnumber] = re.sub(r'TK', '', row[fieldnumber])
            row[fieldnumber] = re.sub(r'Tk', '', row[fieldnumber])
            row[fieldnumber] = re.sub(r'\d', '', row[fieldnumber])
            row[fieldnumber] = re.sub(r'\s+', '', row[fieldnumber])
            row[fieldnumber] = re.sub(r'BilukPoh', 'Bilukpoh', row[fieldnumber])
            row[fieldnumber] = re.sub(r'YehPenet', 'Penet', row[fieldnumber])
        rows.updateRow(row)
    del row
    del rows
    return

fields = [0,1]
for x in fields:
    basin_name(input_samples,x)
rows = arcpy.da.UpdateCursor(input_samples, ["RiverName", "NameLocati", "KoordinatL"])
for row in rows:
    if row[2] == "99999999":
        if row[0] == "":
            row[0] = row[1]
    rows.updateRow(row)


arcpy.JoinField_management(input_samples, "RiverName", "Basins_FeatureToPoint", "Basin")
# Переместим непривязанные точки в координаты центроидов соответствующих бассейнов
cursor = arcpy.da.UpdateCursor(input_samples, ["SHAPE@X", "SHAPE@Y", "POINT_X", "POINT_Y", "KoordinatL"])
for row in cursor:
    if row[4] == "99999999" and row[2] is not None:
        row[0] = row[2]
        row[1] = row[3]
    cursor.updateRow(row)
del row
del cursor

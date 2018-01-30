# coding: utf8
import sys, arcpy, re, openpyxl
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

arcpy.env.workspace = "D:/YandexDisk/Projects/Bali/Bali.gdb"
input = "AirDanau"
input_samples = arcpy.Copy_management(input, "AirDanau_Copy")

# Переместим непривязанные точки в координаты точек с такой же локацией в атрибутах
rows = arcpy.da.UpdateCursor(input_samples, ["SHAPE@X", "SHAPE@Y", "KoordinatL", "NameLocati"])
for row in rows:
    if row[2] == "99999999":
        Location = row[3]
        rows2 = arcpy.da.SearchCursor(input_samples, ["SHAPE@X", "SHAPE@Y", "KoordinatL", "NameLocati"])
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
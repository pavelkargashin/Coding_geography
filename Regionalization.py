# coding: utf8
import sys, arcpy, os, parameters, re
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True
arcpy.env.workspace = parameters.ProjectFolder + "/Bali.gdb"
# Local variables:
Basins = "Basins"
samples = "AirSungai_Copy" # Сюда на вход должны подаваться пробы, разбитые по средам, годам и месяцам

# Process: Identity
samples_identity = arcpy.Identity_analysis(samples, Basins, str(samples) + "_Identity", "ALL", "", "NO_RELATIONSHIPS")

field_names = [f.name for f in arcpy.ListFields(samples_identity)]
fields = []
for item in field_names[13:]: #список полей с показателями
    item_renamed = str(item)
    fields.append(item_renamed)
rows = arcpy.da.UpdateCursor(samples_identity, fields) # замена всех значений 999999999 на Null
for row in rows:
    for field in fields:
        if row[fields.index(field)] == 99999999:
            row[fields.index(field)] = None
            rows.updateRow(row)
def dissolving_fields(fields, stats): # функция для создания текстового аргумента расчёта статистики в инструменте Dissolve
    i = len(fields)
    text = ""
    for field in fields:
        x = 1
        text0 = str(field) + " " + str(stats)
        x = x + 1
        if x < i:
            text0 = str(text0) + ";"
        text = text + text0
    return text
text = dissolving_fields(fields, "MAX") # Расчет максимальных показателей
# Process: Dissolve
Samples_Dissolve = arcpy.Dissolve_management(samples_identity, str(samples) + "_Dissolve", "Basin_1", text,
                                             "MULTI_PART", "DISSOLVE_LINES")

# Полигональный класс бассейнов
arcpy.SpatialJoin_analysis(Basins, Samples_Dissolve, "Basins_Samples", "JOIN_ONE_TO_ONE", "KEEP_ALL")
# Создание серии карт по тематическим показателям
fields = [f.name for f in arcpy.ListFields("Basins_Samples")]
mxd = arcpy.mapping.MapDocument(str(parameters.ProjectFolder) + "/Bali_scripting.mxd")
df = arcpy.mapping.ListDataFrames(mxd)[0]
lyr = arcpy.mapping.ListLayers(mxd, "Basins_Samples_2", df)[0]
lyrFile = arcpy.mapping.Layer("Basins_Samples.lyr")
for field in fields[13:-9]:
    print field
    arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)
    lyr.symbology.reclassify()
    lyr.symbology.valueField = str(field)
    lyr.symbology.numClasses = 5
    lyr.name = str(re.sub(r'_', ' ', field))
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
    legend.autoAdd = True
    arcpy.mapping.AddLayer(df, lyr, "BOTTOM")
    arcpy.mapping.ExportToPNG(mxd, parameters.OutputData + "/" + str(field)+ ".png")
    legend.removeItem(legend.listLegendItemLayers()[0])


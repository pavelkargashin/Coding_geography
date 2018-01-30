# coding: utf8
import sys, arcpy
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True
arcpy.env.workspace = "D:/YandexDisk/Projects/Bali/Bali.gdb"
# Local variables:
Basins = "Basins"
samples = "AirSungai_Copy" # Сюда на вход должны подаваться пробы, разбитые по средам, годам и месяцам

# Process: Identity
Samples_Identity = arcpy.Identity_analysis(samples, Basins, str(samples) + "_Identity", "ALL", "", "NO_RELATIONSHIPS")

field_names = [f.name for f in arcpy.ListFields(Samples_Identity)]
fields = field_names[13:] #список полей с показателями
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
Samples_Dissolve = arcpy.Dissolve_management(Samples_Identity, str(samples) + "_Dissolve", "Basin_1", text,
                                             "MULTI_PART", "DISSOLVE_LINES")

# Полигональный класс бассейнов
arcpy.SpatialJoin_analysis(Basins, Samples_Dissolve, "Basins_Samples", "JOIN_ONE_TO_ONE", "KEEP_ALL")



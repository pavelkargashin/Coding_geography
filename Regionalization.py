# coding: utf8
import sys, arcpy, os, parameters, re
import parameters
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

def update_fields(input_fc_identity):
    field_names = [f.name for f in arcpy.ListFields(input_fc_identity)]
    fields = []
    for item in field_names[13:]: #список полей с показателями
        item_renamed = str(item)
        fields.append(item_renamed)
    rows = arcpy.da.UpdateCursor(input_fc_identity, fields) # замена всех значений 999999999 на Null
    for row in rows:
        for field in fields:
            if row[fields.index(field)] == 99999999:
                row[fields.index(field)] = None
                rows.updateRow(row)
    return fields


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



def regionalisation_process(samples, Basins, tempGISFolder):
# Process: Identity
    samples_identity = arcpy.Identity_analysis(samples, Basins, tempGISFolder+"/Samples_Identity", "ALL", "", "NO_RELATIONSHIPS")
    arcpy.env.workspace = tempGISFolder
    fields2process = update_fields(samples_identity)
    text = dissolving_fields(fields2process, "MAX") # Расчет максимальных показателей
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
    for field in fields[13:]:
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

if __name__ == "__main__":
    GISFolder = parameters.ProjectFolder+parameters.GISDataName+'.gdb'
    InputThematic = GISFolder+parameters.ThematicDatasetName
    InputBaseMap = GISFolder+parameters.BasemapDatasetName
    tempGISFolder = GISFolder+parameters.AnalysisDatasetName

    samples = InputThematic+"/AirDanau_2009_April"
    Basin = InputBaseMap+'/Basins'
    regionalisation_process(samples, Basin, tempGISFolder)


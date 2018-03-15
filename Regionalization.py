# coding: utf8
import sys, arcpy, os, parameters, re
import databaseTools, parameters_test, configparser
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

def update_fields(input_fc_identity, start_field):
    field_names = [f.name for f in arcpy.ListFields(input_fc_identity)]
    fields = field_names[start_field:]
    rows = arcpy.da.UpdateCursor(input_fc_identity, fields) # замена всех значений 999999999 на Null
    for row in rows:
        for field in fields:
            if row[fields.index(field)] == 99999999 or row[fields.index(field)] == "99999999":
                row[fields.index(field)] = None
        rows.updateRow(row)
    del row
    del rows
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

def get_initial_data(inputdataset, outputdataset, env, year):
    arcpy.env.workspace = inputdataset
    tempdataset = outputdataset
    searchCriteria = env + '_' + year + '*'
    listFC = arcpy.ListFeatureClasses(wild_card=searchCriteria)
    datas = set()
    for item in listFC:
        splitName = re.split(r'_', item)
        data = splitName[0] + '_' + splitName[1]
        datas.add(data)
    for item in datas:
        templistfc = arcpy.ListFeatureClasses(item + '*')
        arcpy.Merge_management(templistfc, tempdataset + '/' + item)



def regionalisation_process(samples, Basins, tempGISFolder, year, env):
    # Process: Identity
    Basins_Multy = tempGISFolder+"/Basins_Multy"
    arcpy.MultipartToSinglepart_management(Basins, Basins_Multy)
    samples_identity = arcpy.Identity_analysis(samples, Basins_Multy, tempGISFolder+"/Samples_Identity", "ALL", "", "NO_RELATIONSHIPS")
    arcpy.env.workspace = tempGISFolder
    fields2process = update_fields(samples_identity, 13)
    text = dissolving_fields(fields2process[:-5], "MAX") # Расчет максимальных показателей
    # Process: Dissolve
    Samples_Dissolve = arcpy.Dissolve_management(samples_identity, str(samples) + "_Dissolve", "Basin", text,
                                                 "SINGLE_PART", "DISSOLVE_LINES")

    # Полигональный класс бассейнов
    arcpy.SpatialJoin_analysis(Basins_Multy, Samples_Dissolve, "Basins_Samples", "JOIN_ONE_TO_ONE", "KEEP_ALL")
    # Создание серии карт по тематическим показателям
    fields = [f.name for f in arcpy.ListFields("Basins_Samples")]
    mxd = arcpy.mapping.MapDocument(str(parameters.ProjectFolder) + "Bali_scripting1.mxd")
    print mxd.filePath, mxd.title
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    lyr = arcpy.mapping.ListLayers(mxd, "Basins_Samples", df)[0]
    if lyr.isBroken == True:
        lyr.replaceDataSource(parameters.ProjectFolder, "SHAPEFILE_WORKSPACE")
        lyr.save()
    lyrFile = arcpy.mapping.Layer(parameters.ProjectFolder+"/Basins_Samples_1.lyr")
    lyrFile_inverted = arcpy.mapping.Layer(parameters.ProjectFolder + "/Basins_Samples_2.lyr")
    for field in fields[11:-2]:
        print field
        fieldData = databaseTools.extract_unique_values("Basins_Samples", field)
        if len(fieldData) == 1 and fieldData[0] == None:
            continue
        else:
            lyr.name = str(re.sub(r'_', ' ', field))
            if field == "MAX_DO_mgL":
                print "inverted"
                arcpy.mapping.UpdateLayer(df, lyr, lyrFile_inverted, True)
            else:
                arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)
                print "direct"
            lyr.symbology.reclassify()
            lyr.symbology.valueField = str(field)
            breaks_ini = parameters_test.get_setting(r'd:\YandexDisk\Projects\Bali_Test\\', r'CONFIGURATION.ini',
                                                     "BreakValues", setting=str(field)[4:])
            separated = breaks_ini[1:-1].split(", ")
            max = len(separated)
            print separated
            labels = []
            label_first = "Less than " + separated[1]
            labels.append(label_first)
            for i in range(1,max-2):
                label = separated[i] + " - " + separated[i+1]
                labels.append(label)
            label_last = "More than " + separated[max - 2]
            labels.append(label_last)
            print labels
            breaks = []
            for item in separated:
                item_float = float(item)
                breaks.append(item_float)
            print breaks
            lyr.symbology.classBreakValues = breaks
            lyr.symbology.classBreakLabels = labels
            titleItem = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]
            titleItem.text = str(year)
            arcpy.mapping.ExportToPNG(mxd, parameters.OutputData + "/" + env+'_'+year+'_'+str(field) + ".png")



if __name__ == "__main__":

    GISFolder = parameters.ProjectFolder+parameters.GISDataName+'.gdb'
    InputThematic = GISFolder+'/'+parameters.ThematicDatasetName
    InputBaseMap = GISFolder+'/'+parameters.BasemapDatasetName
    tempGISFolder = GISFolder+'/'+parameters.AnalysisDatasetName
    Basin = parameters.polyg_name_dict[parameters.Sungai]
    years = ['2009', '2011', '2012', '2013', '2014', '2016']
    #years = ['2016']
    for year in years:
        #year = '2014'
        env = 'AirSungai'
        #searchCriteria = env+'_'+year+'*'
        searchCriteria = env + '_' + year

        #get_initial_data(InputThematic, tempGISFolder, env, year)
        arcpy.env.workspace = tempGISFolder

        samples = InputThematic + '/' + searchCriteria
        regionalisation_process(samples, Basin, tempGISFolder, year, env)

    # listFC = arcpy.ListFeatureClasses(wild_card=searchCriteria)
    # print listFC
    # for item in listFC:
    #     samples = tempGISFolder+'/'+item
    #     print samples
    #     regionalisation_process(samples, Basin, tempGISFolder, year, env)


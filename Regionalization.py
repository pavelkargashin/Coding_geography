# coding: utf8
import sys, arcpy, parameters, re, os
import databaseTools, parameters_test, databaseAnalysis
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

def update_fields(input_fc_identity):
    field_names = [f.name for f in arcpy.ListFields(input_fc_identity)]
    rows = arcpy.da.UpdateCursor(input_fc_identity, field_names) # Replacement of 999999999 on Null values
    for row in rows:
        for field in field_names:
            if row[field_names.index(field)] == 99999999 or row[field_names.index(field)] == "99999999":
                row[field_names.index(field)] = None
        rows.updateRow(row)
    del row
    del rows
    return field_names

def dissolving_fields(fields, stats): # Creation of text argument for statistics calculation in dissolve tool
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

def regionalisation_process(GISFolder, regions, env, stats, years, indexes):
    InputThematic = GISFolder + '/' + parameters.ThematicDatasetName
    InputBaseMap = GISFolder + '/' + parameters.BasemapDatasetName
    tempGISFolder = GISFolder + '/' + parameters.AnalysisDatasetName
    arcpy.env.workspace = tempGISFolder
    # Creation of merged feature class within which statistics should be calculated
    env_data = databaseAnalysis.create_fc_environment(InputThematic, env, tempGISFolder)
    # Field names extraction
    field_names = [f.name for f in arcpy.ListFields(env_data, field_type="Double")]
    # Comparison of input indexes with existing in the attribute table and creation of intersecting list
    mapping_fields = list(set(field_names) & set(indexes))
    # Adding section to configuration file
    section_name = databaseAnalysis.add_section(parameters.ProjectFolder, "CONFIGURATION.ini", env)
    # Statistics analysis for break values calculation
    for field in mapping_fields:
        breaks = databaseAnalysis.find_breaks(env_data, field)
        # Writing breaks to configuration file
        databaseAnalysis.set_current_config(parameters.ProjectFolder, "CONFIGURATION.ini", section_name, field, breaks)
    # Searching feature_classes based on parameters
    for year in years:
        searchCriteria = env + '_' + year
        samples = InputThematic + '/' + searchCriteria
        # Disaggregating of multipart feature class
        regions_multy = arcpy.MultipartToSinglepart_management(regions, tempGISFolder+"/Regions_Multy")
        # Overlay of samples with regions
        samples_identity = arcpy.Identity_analysis(samples, regions_multy, tempGISFolder+"/Samples_Identity", "ALL", "",
                                                   "NO_RELATIONSHIPS")
        # Replacement of 9999999 values on None on attribute table
        update_fields(samples_identity)
        # Creation of text argument for statistics calculation
        text = dissolving_fields(mapping_fields, stats) # calculation of statistics
        # Dissolving samples within regions and calculation of statistics
        samples_dissolve = arcpy.Dissolve_management(samples_identity, str(samples) + "_Dissolve",
                                                     parameters.polyg_attr_name_dict[env], text, "SINGLE_PART",
                                                     "DISSOLVE_LINES")
        # Spatial join of dissolved samples and regions
        regionalized_samples = arcpy.SpatialJoin_analysis(regions_multy, samples_dissolve, tempGISFolder +
                                                          "/Regionalized_Samples", "JOIN_ONE_TO_ONE", "KEEP_ALL")
        arcpy.Delete_management(samples_dissolve)
        # Creation of map series based on parameters
        # Arcmap map project file
        mxd = arcpy.mapping.MapDocument(str(parameters.ProjectFolder) + "Bali_scripting1.mxd")
        # Dataframe
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        lyr = arcpy.mapping.ListLayers(mxd, "Regionalized_Samples", df)[0]
        lyrFile = arcpy.mapping.Layer(parameters.ProjectFolder+"/Regionalized_Samples_1.lyr")
        lyrFile_inverted = arcpy.mapping.Layer(parameters.ProjectFolder + "/Regionalized_Samples_2.lyr")
        for field in mapping_fields:
            stat_field = str(stats) + "_" + str(field)
            fieldData = databaseTools.extract_unique_values(regionalized_samples, stat_field)
            if fieldData[0] == None:
                fieldData.remove(None)
            elif len(fieldData) == 0:
                continue
            # Replacing symbols in layer name in legend
            lyr.name0 = str(re.sub(r'_', ' ', stat_field))
            lyr.name = str(re.sub(r'mgL', 'mg/L', lyr.name0))
            # Applying direct or inverted color scheme
            if stat_field == stats + "_" + "DO_mgL":
                arcpy.mapping.UpdateLayer(df, lyr, lyrFile_inverted, True)
            else:
                arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)
            lyr.symbology.reclassify()
            lyr.symbology.valueField = stat_field
            breaks_ini = parameters_test.get_setting(parameters.ProjectFolder, r'CONFIGURATION.ini',
                                                     section_name, setting=str(field))
            # Creating labels for legend
            separated = breaks_ini[1:-1].split(", ")
            max = len(separated)
            labels = []
            label_first = "Less than " + separated[1]
            labels.append(label_first)
            for i in range(1,max-2):
                label = separated[i] + " - " + separated[i+1]
                labels.append(label)
            label_last = "More than " + separated[max - 2]
            labels.append(label_last)
            # Creating break value list
            breaks = []
            for item in separated:
                item_float = float(item)
                breaks.append(item_float)
            lyr.symbology.classBreakValues = breaks
            lyr.symbology.classBreakLabels = labels
            # Creating current year of the samples title
            titleItem = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]
            titleItem.text = str(year)
            arcpy.mapping.ExportToPNG(mxd, parameters.OutputData + "/" + env+'_'+year+'_'+str(stat_field) + '_'+str(os.path.basename(regions)) + ".png",
                                      resolution=300)

if __name__ == "__main__":

    GISFolder = parameters.ProjectFolder+parameters.GISDataName+'.gdb'
    regions = parameters.polyg_name_dict[parameters.Sungai]
    env = parameters.Sungai
    stats = "MAX"
    years = ['2009', '2011', '2012', '2013', '2014', '2016']
    indexes = parameters.field_list_sungai
    regionalisation_process(GISFolder, regions, env, stats, years, indexes)



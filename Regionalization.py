# coding: utf8
import sys, arcpy, re, os
import databaseTools, databaseAnalysis, General_Tools_ConfigFile as GTC
arcpy.env.overwriteOutput=True
config_file = "CONFIGURATION.ini"
paths = "Paths"

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
        x = 0
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
        arcpy.Merge_management(templistfc, tempdataset + '\\' + item)


def layer_name_correction(lyr, stats, stat_field):
    lyr.name0 = str(re.sub(r'_', ' ', stat_field))
    if stats == "COUNT":
        lyr.name1 = str(re.sub(r' mgL', '', lyr.name0))
        lyr.name = str(re.sub(r'COUNT', 'Number of samples', lyr.name1))
    else:
        lyr.name = str(re.sub(r'mgL', 'mg/L', lyr.name0))
    return lyr.name


def legend_labeling(breaks_ini, lyr):
    separated = breaks_ini[1:-1].split(", ")
    max = len(separated)
    labels = []
    label_first = "Less than " + separated[1]
    labels.append(label_first)
    for i in range(1, max - 2):
        label = separated[i] + " - " + separated[i + 1]
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
    return lyr


def making_map(mxd, env, year, stat_field, regions):
    titleItem = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")[0]
    titleItem.text = str(year)
    project_folder = GTC.get_setting(config_file, paths, "projectfolder")
    path = project_folder + "OutputData" + "\\" + env + '_' + str(year) + '_' + str(stat_field) + '_' + str(
        os.path.basename(regions)) + ".png"
    arcpy.AddMessage(path)
    arcpy.mapping.ExportToPNG(mxd, path, resolution=300)


def regionalisation_process(GISFolder, regions, env, stats, years, value_list):
    # If script runs from ArcGIS
    project_folder = GISFolder.split(GTC.get_setting(config_file, paths, "gisdataname") + ".gdb")[0]
    indexes = re.split(r";", value_list)
    # If script runs without ArcGIS
    GISFolder = project_folder + "\\" + GTC.get_setting(config_file, paths, "gisdataname") + ".gdb"
    InputThematic = GISFolder + '\\' + GTC.get_setting(config_file, paths, "thematicdatasetname")
    InputBaseMap = GISFolder + '\\' + GTC.get_setting(config_file, paths, "basemapdatasetname")
    tempGISFolder = GISFolder + '\\' + GTC.get_setting(config_file, paths, "analysisdatasetname")
    arcpy.env.workspace = tempGISFolder
    # Creation of merged feature class within which statistics should be calculated
    env_data = databaseAnalysis.create_fc_environment(InputThematic, env, tempGISFolder)
    # Adding section to configuration file
    section_name = databaseAnalysis.add_section(project_folder, config_file, env)
    # Searching feature_classes based on parameters
    years_list = re.split(r";", years)
    for year in years_list:
        searchCriteria = env + '_' + str(year)
        samples = InputThematic + '\\' + searchCriteria
        # Disaggregating of multipart feature class
        regions_multy = arcpy.MultipartToSinglepart_management(regions, tempGISFolder+"\\Regions_Multy")
        # Overlay of samples with regions
        samples_identity = arcpy.Identity_analysis(samples, regions_multy, tempGISFolder+"\\Samples_Identity", "ALL", "",
                                                   "NO_RELATIONSHIPS")
        # Replacement of 9999999 values on None on attribute table
        update_fields(samples_identity)
        # Creation of text argument for statistics calculation
        text = dissolving_fields(indexes, stats) # calculation of statistics
        # Dissolving samples within regions and calculation of statistics
        dict = GTC.read_as_dict(config_file, "Dictionaries", "polyg_attr_name_dict_keys", "polyg_attr_name_dict_values")
        samples_dissolve = arcpy.Dissolve_management(samples_identity, str(samples) + "_Dissolve", dict[env],
                                                     text, "MULTI_PART", "DISSOLVE_LINES")
        # Spatial join of dissolved samples and regions
        regionalized_samples = arcpy.SpatialJoin_analysis(regions_multy, samples_dissolve, tempGISFolder +
                                                          "\\Regionalized_Samples", "JOIN_ONE_TO_ONE", "KEEP_ALL")
        arcpy.Delete_management(samples_dissolve)
        # Creation of map series based on parameters
        # Arcmap map project file
        mxd = arcpy.mapping.MapDocument(str(project_folder) + "Bali_scripting1.mxd")
        # Dataframe
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        lyr = arcpy.mapping.ListLayers(mxd, "Regionalized_Samples", df)[0]
        lyrFile = arcpy.mapping.Layer(project_folder+"\\Regionalized_Samples_1.lyr")
        lyrFile_inverted = arcpy.mapping.Layer(project_folder + "\\Regionalized_Samples_2.lyr")
        lyrFile_count = arcpy.mapping.Layer(project_folder + "\\Regionalized_Samples_3.lyr")
        for field in indexes:
            stat_field = str(stats) + "_" + str(field)
            fieldData = databaseTools.extract_unique_values(regionalized_samples, stat_field)
            if fieldData[0] == None:
                fieldData.remove(None)
            elif len(fieldData) == 0:
                continue
            # Applying direct or inverted color scheme
            if stats == "COUNT":
                layer_name_correction(lyr, stats, stat_field)
                arcpy.mapping.UpdateLayer(df, lyr, lyrFile_count, True)
                arcpy.AddField_management(regionalized_samples, "Count_Samples", "SHORT")
                rows = arcpy.da.UpdateCursor(regionalized_samples, [stat_field, "Count_Samples"])
                for row in rows:
                    row[1] = row[0]
                    rows.updateRow(row)
                del row
                del rows
                arcpy.mapping.UpdateLayer(df, lyr, lyrFile_count, True)
            else:
                # Statistics analysis for break values calculation
                for field in indexes:
                    breaks = databaseAnalysis.find_breaks(env_data, field)
                    # Writing breaks to configuration file
                    databaseAnalysis.set_current_config(project_folder, config_file, section_name, field, breaks)
                layer_name_correction(lyr, stats, stat_field)
                if stat_field == stats + "_" + "DO_mgL":
                    arcpy.mapping.UpdateLayer(df, lyr, lyrFile_inverted, True)
                else:
                    arcpy.mapping.UpdateLayer(df, lyr, lyrFile, True)
                lyr.symbology.reclassify()
                lyr.symbology.valueField = stat_field
                breaks_ini = GTC.get_setting(project_folder, config_file, section_name, setting=str(field))
                legend_labeling(breaks_ini, lyr)
            making_map(mxd, env, year, stat_field, regions)
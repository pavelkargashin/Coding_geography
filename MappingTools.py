import arcpy
import configparser
mxd = arcpy.mapping.MapDocument(str(parameters.ProjectFolder) + "Bali_scripting1.mxd")
    print mxd.filePath, mxd.title
    df = arcpy.mapping.ListDataFrames(mxd)[0]
import arcpy
import os
import configparser
import parameters_test
Path2GIS = 'C:/PAUL/AAGISTesting/MYGIS/GISEcologyBali.gdb'

DataSource = 'AirSungai_2014_September'
mxdName = 'C:/PAUL/AAGISTesting/MYGIS/GISEcologyBali.mxd'
lyrName = 'C:/PAUL/AAGISTesting/MYGIS/Decoration/SimpleThematic.lyr'
outputFolder = 'C:/PAUL/AAGISTesting/MYGIS/OutputData'

def create_simplemap(mxdName, lyrName, Path2GIS, DataSource, outputFolder):
    mxd = arcpy.mapping.MapDocument(mxdName)

    df = arcpy.mapping.ListDataFrames(mxd)[0]
    myLayer = arcpy.mapping.Layer(lyrName)
    arcpy.mapping.AddLayer(df, myLayer)

    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT", "Legend")[0]
    legend.autoAdd = True
    myLayer.replaceDataSource(Path2GIS, "FILEGDB_WORKSPACE",DataSource )
    print myLayer.dataSource
    print myLayer.symbologyType

    myLayer.symbology.valueField = 'NO2_mgL'
    mxd.save()



    arcpy.mapping.ExportToPNG(mxd, outputFolder + "/" + 'ThematicNew' + ".png")
    del mxd
    return
#
# def save_temCopy(mxdName):
#     mxd = arcpy.mapping.MapDocument(mxdName)
#     mxdTemp = os.path.splitext(mxd)[0] + '_temp.mxd'
#     mxd.saveACopy(mxdTemp)
#     return mxdTemp


create_simplemap(mxdName, lyrName, Path2GIS, DataSource, outputFolder)

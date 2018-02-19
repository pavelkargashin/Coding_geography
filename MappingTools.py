import arcpy
import configparser
mxdName = 'C:/PAUL/AAGISTesting/MYGIS/GISEcologyBali.mxd'
def appendlayer(mxdName):
    df = arcpy.mapping.ListDataFrames(mxdName)[0]

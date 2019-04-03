#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
import shutil
import General_Tools_ConfigFile as GTC
import Create_Exec_ImportBasemap
import Create_Exec_ImportThematic
import Create_Exec_DatabaseProcessing

home = os.getenv("HOME")




def SelectThematic(ThematicFileName, ConfigFileName):
    pathToCopy = GTC.get_setting(ConfigFileName, Paths, 'inputdata')
    dstFileName = pathToCopy+os.path.basename(ThematicFileName)
    shutil.copy(ThematicFileName, dstFileName)
    print 'Thematic data has been copied!'
    ThematicFileName = dstFileName
    print 'Data will be imported from ',ThematicFileName
    return ThematicFileName


def SelectBasemap(BaseMapFolder, ConfigFileName):
    pathToCopy = GTC.get_setting(ConfigFileName, Paths, 'inputdata')
    for item in os.listdir(BaseMapFolder):
        shutil.copy(BaseMapFolder+item, pathToCopy+item)
    print 'Shapefiles have been copied!'
    return


def runImport(ConfigFileName, ThematicFileName):
    Create_Exec_ImportBasemap.main(ConfigFileName)
    inputFolder = GTC.get_setting(ConfigFileName, Paths, 'inputdata')
    # Convert thematic data to shapefiles
    excelName = ThematicFileName
    dstFileName = os.path.basename(str(excelName))
    print dstFileName
    outputFolder = GTC.get_setting(ConfigFileName, Paths, 'tempdata')
    Create_Exec_ImportThematic.main(inputFolder, dstFileName, "Air", outputFolder)
    # Import data to geodatabase
    inputfolder_shp = GTC.get_setting(ConfigFileName, Paths, 'tempdata')
    envDatabase = GTC.get_setting(ConfigFileName, Paths, 'projectfolder')\
                  +GTC.get_setting(ConfigFileName, Paths, 'gisdataname') + '.gdb'
    ThematicDataset = envDatabase + '/' + GTC.get_setting(ConfigFileName, Paths, 'thematicdatasetname')
    fieldname = GTC.get_setting(ConfigFileName, 'ImportParameters', 'fieldname')
    fieldname_2 = GTC.get_setting(ConfigFileName, 'ImportParameters', 'fieldname_2')
    Create_Exec_DatabaseProcessing.main(inputfolder_shp, envDatabase, ThematicDataset, fieldname, fieldname_2)
    return


def main(ThematicFileName, ConfigFileName, BaseMapFolder):
    SelectBasemap(BaseMapFolder, ConfigFileName)
    temp_thematic_file = SelectThematic(ThematicFileName, ConfigFileName)
    runImport(temp_thematic_file, ConfigFileName)
    print' All done'

if __name__=='__main__':
    Paths = 'Paths'
    ThematicFileName = sys.argv[1]
    ConfigFileName = sys.argv[2]
    BaseMapFolder = sys.argv[3]
    main(ThematicFileName, ConfigFileName, BaseMapFolder)
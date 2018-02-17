import os
import time
import arcpy



ProjectFile = ProjectFolder+mxdName
def create_mxd_v1(FutureFile):
    open(ProjectFile, 'w').close()
    os.startfile(ProjectFile)
    time.sleep(120)
    os.system("taskkill /f /im arcmap.exe")
    mxd = arcpy.mapping.MapDocument(ProjectFile)
    print mxd.dateSaved

create_mxd_v1(ProjectFile)


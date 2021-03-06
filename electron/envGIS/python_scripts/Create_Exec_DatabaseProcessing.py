# -*- coding:utf-8-*-
import arcpy
import re
import Create_Tools_MakeShapefiles


def main(inputfolder_shp, envDatabase, ThematicDataset, fieldname, fieldname_2):

    # Импорт в БГД и разделение по году
    arcpy.RefreshCatalog(envDatabase)
    arcpy.env.overwriteOutput = True
    files2process = Create_Tools_MakeShapefiles.select_shapefiles(inputfolder_shp)
    for item in files2process:
        newfilename = re.sub(r'\.shp','', item)
        outputfile = ThematicDataset+'/'+newfilename
        Create_Tools_MakeShapefiles.split_data_year(inputfolder_shp + item, outputfile, fieldname)
    print '\n#####################\nImport Stage 1 has been finished\n#####################\n'
    # Разделение по этапу мониторинга
    arcpy.RefreshCatalog(envDatabase)
    fc2process = Create_Tools_MakeShapefiles.list_feature_classes(ThematicDataset)
    for item in fc2process:
        Create_Tools_MakeShapefiles.split_data_stage(ThematicDataset + '/' + item, ThematicDataset + '/' + item, fieldname_2)
        # arcpy.Delete_management(ThematicDataset+'/'+item) #Пока строка не используется. до тех пор пока не будет поправлен файл Maps_Tools_Regionalization.py

    print '\n#####################\nFin\n#####################\n\nAll data is in GIS!\nNow you can work with it!!!'

if __name__ == "__main__":
    main()

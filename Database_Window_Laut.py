# -*-coding:utf-8-*-
import sys
import csv
import General_Tools_ConfigFile as GTC



def create_csv(filename, fieldlist):
    with open(filename, 'wb') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(fieldlist)


def write_to_csv(indatalist, destfile):
    print ("write data to Excel file!")
    with open(destfile, 'ab') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(indatalist)
    print('Your data has been appended!')



def main(inputlist, fileName, field_list_sungai):
    if fileName is True:
        write_to_csv(inputlist, fileName)
    else:
        create_csv(fileName, field_list_sungai)
        write_to_csv(inputlist, fileName)



if __name__=='__main__':
    inputlist = sys.argv[1]

    filePath = filePath = GTC.get_setting('CONFIGURATION', 'Paths', 'inputdata')
    fileName = filePath+"Laut_add.csv"
    field_list_laut = [u'Point', u'Location', u'Longitude',
                         u'Latitude', u'Year', u'Stage',
                         u'Color_CU', u'Smell', u'Brightness',
                         u'Turbidity_', u'TSS_mgL', u'Waste',
                         u'OilCoating', u'Temperatur', u'pH',
                         u'Salinity_m', u'DO_mgL', u'BOD5_mgL',
                         u'COD_mgL', u'TotalAmmon', u'NO2_N_mgL',
                         u'NO3_N_mgL', u'PO4_P_mgL', u'Cyanide_mg',
                         u'Sulfide_mg',  u'FreeChlori', u'CrudeOil_m',
                         u'Phenol_mgL', u'Pesticide_', u'PCB_mgL',
                         u'Phospat_mg', u'Cd_mgL', u'TotalColif']

    main(inputlist, fileName, field_list_laut)



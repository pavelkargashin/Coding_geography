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
    configFileName = sys.argv[1]
    inputlist = sys.argv[2]
    filePath = GTC.get_setting(configFileName, 'Paths', 'inputdata')
    fileName = filePath+"Sumur_add.csv"
    field_list_sumur = [u'Area', u'Location', u'Longitude',
                     u'Latitude', u'Year', u'Stage', u'Temperatur',
                     u'TDS_mgL', u'TSS_mgL', u'pH',  u'BOD_mgL', u'COD_mgL',
                     u'DO_mgL', u'TotalP_mgL', u'NO3_N_mgL', u'NH3_N_mgL',
                     u'As_mgL', u'Co_mgL', u'Ba_mgL', u'B_mgL', u'Se_mgL',
                     u'Cd_mgL', u'Cr_V_mgLI', u'Cu_mgL', u'Fe_mgL',  u'Pb_mgL',
                     u'Mn_mgL', u'Hg_mgL', u'Zn_mgL', u'Chloride_m', u'Cyanide_mg',
                     u'Fluoride_m', u'NO2_N_mgL', u'Sulphate_m', u'FreeChlori',
                     u'Sulfide_mg', u'Salinity_m', u'FecalColif', u'TotalColif',
                     u'Gloss_A_mg', u'Gloss_B_mg', u'DHL_mgL', u'Phenol_mgL',
                     u'OilAndFat_', u'Detergent_',  u'PO4_mgL', u'Turbidity_']
    main(inputlist, fileName, field_list_sumur)

#-*-coding:utf-8-*-
import os
import csv
import openpyxl
import sys

TestDataFolder = 'C:/PAUL/Science/GISofBALI/DataSource/'
workData = 'StatData.xlsx'
exceldata = TestDataFolder+workData

# myExcel = openpyxl.load_workbook(TestDataFolder+workData)
# mySheets = myExcel.get_sheet_names()#get all shhets via list
# currentSheet = mySheets[0] #get the first sheet as a list object
# mySheet = myExcel.get_sheet_by_name(currentSheet)#reach the sheet as object for further work
# all_records = []
# list_keys = []
# # Create list of keys for dictionary. Extract them from the first row
# for item in range(1, mySheet.max_column+1, 1):
#    list_keys.append(mySheet.cell(column = item, row = 1).value)
#
# # myDoc = open(TestDataFolder+'TEST.txt', 'w')
#
# list_temp = []
# for row_val in range(2, 5):
#     print row_val
#     for col_val in range(1, mySheet.max_column+1):
#         print col_val, mySheet.cell(column=col_val, row=row_val).value
#
#         list_temp.append(mySheet.cell(column=col_val, row=row_val).value)
#     record = dict(zip(list_keys, list_temp))
#     all_records.append(record)
#     list_temp = []
#     record = {}

def explore_workbook(inputexcel):
    myExcel = openpyxl.load_workbook(inputexcel)
    mySheets = myExcel.get_sheet_names()  # get all sheets via list
    myDoc = open(TestDataFolder + 'TEST.txt', 'w')
    for item in mySheets:
        myDoc.write(item)
    myDoc.close()


def export_data_to_csv(inputexcel, currentSheet):
    myExcel = openpyxl.load_workbook(inputexcel)
    mySheet = myExcel.get_sheet_by_name(currentSheet)
    with open("new_csv.csv", 'wb') as mycsv:
        filewriter = csv.writer(mycsv)
        for row in xrange(mySheet.rows()):
            filewriter.writerow(mySheet.values(row).encode('utf-8'))
    mycsv.close()


def create_fields_list(inputexcel, currentSheet):
    list_temp = []
    myExcel = openpyxl.load_workbook(inputexcel)
    mySheet = myExcel.get_sheet_by_name(currentSheet)
    row_val=1
    with open(TestDataFolder+'attrNames.csv', 'w') as curCsv:
        MyWriter = csv.writer(curCsv, delimiter = ',')

        for col_val in range(1, mySheet.max_column+1):
            print (mySheet.cell(column=col_val, row=row_val).value)
            list_temp.append(mySheet.cell(column=col_val, row=1).value)
        MyWriter.writerow(list_temp)
        curCsv.close()

    return list_temp

print(create_fields_list(exceldata, "glossary")[0])
# def create_shapefile():

# def fill_shapefile():




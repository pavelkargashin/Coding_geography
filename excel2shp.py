#-*-coding:utf-8-*-
import os
import csv
import openpyxl
import sys

TestDataFolder = 'C:/PAUL/Science/GISofBALI/DataSource/'
workData = 'StatData.xlsx'

myExcel = openpyxl.load_workbook(TestDataFolder+workData)
mySheets = myExcel.get_sheet_names()#get all shhets via list
currentSheet = mySheets[0] #get the first sheet as a list object
mySheet = myExcel.get_sheet_by_name(currentSheet)#reach the sheet as object for further work
all_records = []
list_keys = []
# Create list of keys for dictionary. Extract them from the first row
for item in range(1, mySheet.max_column+1, 1):
   list_keys.append(mySheet.cell(column = item, row = 1).value)

myDoc = open(TestDataFolder+'TEST.txt', 'w')

list_temp = []
for row_val in range(2, 5):
    print row_val
    for col_val in range(1, mySheet.max_column+1):
        print col_val, mySheet.cell(column=col_val, row=row_val).value

        list_temp.append(mySheet.cell(column=col_val, row=row_val).value)
    record = dict(zip(list_keys, list_temp))
    all_records.append(record)
    list_temp = []
    record = {}

print len(all_records)
for item in all_records:
    print item

with open("new_csv.csv", 'wb') as mycsv:
    filewriter = csv.writer(mycsv)
    for item in all_records:
        filewriter.writerows(item.items)
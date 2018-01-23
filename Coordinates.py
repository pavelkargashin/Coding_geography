# coding: utf8
import sys, arcpy, re, openpyxl
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True


wb = openpyxl.load_workbook(filename = "D:\\YandexDisk\\Projects\\Bali\\BALI_GIS_DATA_180120.xlsx")
sheets = wb.get_sheet_names
print(sheets)
Active_Sheet = wb.get_sheet_by_name("SD-14. Kualitas Air Sungai")
Value = Active_Sheet["E2"].value
print Value

text = "115.43''35.2878''"
result = re.split(r"['']", text)
print result[0]
Lon = float(result[0])+float(result[2])/10000
print Lon
# coding: utf8
import sys, arcpy, re, openpyxl
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

# wb = openpyxl.load_workbook(filename = "D:\\YandexDisk\\Projects\\Bali\\BALI_GIS_DATA_180120.xlsx")
# sheets = wb.get_sheet_names
# print(sheets)
# Active_Sheet = wb.get_sheet_by_name("SD-14. Kualitas Air Sungai")
# Value = Active_Sheet["E2"].value
# print Value
def decimating_pseudoDDD(input):
    result0 = re.sub(r"''\.", "''", input)
    result1 = re.split(r"['']", result0)
    Base_Value = float(result1[0]) + float(result1[2]) / 10000
    try:
        Value = Base_Value + float(result1[4])/1000000
    except:
        Value = Base_Value
    return Value

def decimating_pseudoDMS(input):
    result0 = re.sub(r"''\.", ".", input)
    result = re.split(r"['',\.]", result0)
    Value = float(result[0]) + float(result[1])/60 + float(result[3]+"." +result[4])/3600
    return Value

def decimating_DMS(input):
    result0 = re.sub(r"° ", "◦", input)
    result = re.split(r"[◦,']", result0)
    Value = float(result[0]) + float(result[3])/60 + float(result[4])/3600
    return Value

def decimating_FalseDDD(input):
    result = re.split(r"[\.]", input)
    m = float(result[1][0:2])
    tale = result[1][2:]
    power = len(tale)-2
    s = float(tale)/(10**power)
    Value = float(result[0]) + m/60 + s/3600
    return Value

text = "115.240537"
result1 = re.findall(r'[°,◦]', text)
print result1
print len(result1)
if len(result1) is not 0:
    print(decimating_DMS(text))
else:
    result2 = re.findall(r"''", text)
    print len(result2)
    if len(result2) is not 0:
        print "problem"
    else:
        print(decimating_FalseDDD(text))

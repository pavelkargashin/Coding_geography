# coding: utf8
import sys, arcpy, re, openpyxl
reload(sys)
sys.setdefaultencoding('utf8')
arcpy.env.overwriteOutput=True

# Преобразует десятичные градусы вида хх.хх''хх''.хх'' и хх.хх''хх.хх'' в десятичные градусы
def decimating_pseudoDDD(input):
    result0 = re.sub(r"''\.", "''", input)
    result1 = re.split(r"[']+", result0)
    Base_Value = float(result1[0]) + float(result1[1]) / 10000
    try:
        Value = Base_Value + float(result1[2])/1000000
    except:
        Value = Base_Value
    return Value

# Преобразует градусы-минуты-секунды вида хх.хх''хх''.хх'' и хх.хх''хх.хх'' в десятичные градусы
def decimating_pseudoDMS(input):
    result0 = re.sub(r"''\.", ".", input)
    result = re.split(r"['',\.]+", result0)
    print result
    if float(result[1]) < 60 or float(result[2]) < 60:
        Value = float(result[0]) + float(result[1])/60 + float(result[2]+"." +result[3])/3600
    else:
        Value = 0
    return Value

# Преобразует градусы-минуты-секунды вида хх°хх'хх'' в десятичные градусы
def decimating_DMS(input):
    result0 = re.sub(r',', '.', input)
    result00 = re.sub(r"[°◦']+", 'o', result0)
    print "result00="+ str(result00)
    result = re.split(r'o', result00)
    print result
    Value = float(result[0]) + float(result[1])/60 + float(result[2])/3600
    return Value

# Преобразует градусы-минуты-секунды вида xx.xxxxxx в десятичные градусы
def decimating_FalseDDD(input):
    result = re.split(r"[\.]", input)
    m = float(result[1][0:2])
    tale = result[1][2:]
    power = len(tale)-2
    s = float(tale)/(10**power)
    Value = float(result[0]) + m/60 + s/3600
    return Value

# Выбор вариантов обработки
Text = ["8.41''8''.71","114.8''06.70''"]
def Conversion(Text):
    Output = []
    Output_Alternative = []
    if Text[0] == Text[1] == "99999999":
        Output[0] = 9
        Output[1] = 116
        print Output
    else:
        Input = str(Text[0]) + "_" + str(Text[1])
        result1 = re.findall(r"[°◦]", Input)
        print result1
        print len(result1)
        if len(result1) is not 0:
            for Value in Text:
                Output.append(decimating_DMS(Value))
            print Output
        else:
            result2 = re.findall(r"''", Input)
            print len(result2)
            if len(result2) is not 0:
                result3 = re.findall(r"\d'\d", Input)
                if len(result3) is not 0:
                    for Value in Text:
                        Output.append(decimating_pseudoDMS(Value))
                    print Output
                elif decimating_pseudoDMS(Text[0]) == 0 or decimating_pseudoDMS(Text[1]) == 0:
                    for Value in Text:
                        Output.append(decimating_pseudoDDD(Value))
                    print str(Output) + "_decimating_pseudoDDD"
                else:
                    for Value in Text:
                        Output.append(decimating_pseudoDMS(Value))
                        Output_Alternative.append(decimating_pseudoDDD(Value))
                    print str(Output) + "_decimating_pseudoDMS"
                    print str(Output_Alternative) + "_decimating_pseudoDDD"
            else:
                for Value in Text:
                    Output.append(decimating_FalseDDD(Value))
                print Output
    Output[0] = Output[0]*(-1)
    Output_Alternative[0] = Output_Alternative[0]*(-1)
    return Output, Output_Alternative
print str(Conversion(Text))

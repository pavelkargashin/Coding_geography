# coding: utf8
import arcpy, re
arcpy.env.overwriteOutput=True

# Transforming decimal degrees like хх.хх''хх''.хх'' и хх.хх''хх.хх'' in decimal degrees
def decimating_pseudoDDD(input):
    result0 = re.sub(r"''\.", "''", input)
    result1 = re.split(r"[']+", result0)
    Base_Value = float(result1[0]) + float(result1[1]) / 10000
    try:
        Value = Base_Value + float(result1[2])/1000000
    except:
        Value = Base_Value
    return Value

# transforming degrees-minutes-seconds like хх.хх''хх''.хх'' and хх.хх''хх.хх'' in decimal degrees
def decimating_pseudoDMS(input):
    result0 = re.sub(r"''\.", ".", input)
    result = re.split(r"['',\.]+", result0)
    if float(result[1]) < 60 or float(result[2]) < 60:
        Value = float(result[0]) + float(result[1])/60 + float(result[2]+"." +result[3])/3600
    else:
        Value = 0
    return Value

# transforming degrees-minutes-seconds like хх°хх'хх'' in decimal degrees
def decimating_DMS(input):
    result0 = re.sub(r',', '.', input)
    result00 = re.sub(r"[°◦']+", 'o', result0)
    result = re.split(r'o', result00)
    Value = float(result[0]) + float(result[1])/60 + float(result[2])/3600
    return Value

# transforming degrees-minutes-seconds like xx.xxxxxx in decimal degrees
def decimating_FalseDDD(input):
    result = re.split(r"[\.]", input)
    m = float(result[1][0:2])
    tale = result[1][2:]
    power = len(tale)-2
    s = float(tale)/(10**power)
    Value = float(result[0]) + m/60 + s/3600
    return Value

# decision tree for coordinates reading
def Conversion(Text):
    Output = []
    Output_Alternative = []
    # if points have no coordinates
    if Text[0] == Text[1] == "99999999":
        Output.append(float(9))
        Output.append(float(116))
    else:
        Input = str(Text[0]) + "_" + str(Text[1])
        result1 = re.findall(r"[°◦]", Input)
        # if coordinates have symbol "°"
        if len(result1) is not 0:
            for Value in Text:
                Output.append(decimating_DMS(Value))
        else:
            result2 = re.findall(r"''", Input)
            # if coordinates have symbol "''"
            if len(result2) is not 0:
                result3 = re.findall(r"\d'\d", Input)
                # if coordinates have symbol "'"
                if len(result3) is not 0:
                    for Value in Text:
                        Output.append(decimating_pseudoDMS(Value))
                # if coordinates have symbol "'" but minutes or seconds are more than 60
                elif decimating_pseudoDMS(Text[0]) == 0 or decimating_pseudoDMS(Text[1]) == 0:
                    for Value in Text:
                        Output.append(decimating_pseudoDDD(Value))
                else:
                    # reading coordinates with two different functions
                    for Value in Text:
                        Output.append(decimating_pseudoDMS(Value))
                        Output_Alternative.append(decimating_pseudoDDD(Value))
                    # appending key value 1 to the output representing doubts in reading coordinates
                    Output.append(1)
                    Output_Alternative.append(1)
            # if coordinates are likely to be truly decimal
            else:
                # reading coordinates with two different functions
                for Value in Text:
                    Output.append(decimating_FalseDDD(Value))
                    Output_Alternative.append(float(Value))
                # appending key value 1 to the output representing doubts in reading coordinates
                Output.append(1)
                Output_Alternative.append(1)
    # appending key value 0 to the output representing no doubts in reading coordinates
    if len(Output) == 2:
        Output.append(0)
    # don't forget that we are in the southern hemisphere
    Output[0] = Output[0]*(-1)
    if len(Output_Alternative)>0:
        Output_Alternative[0] = Output_Alternative[0]*(-1)
    return Output, Output_Alternative


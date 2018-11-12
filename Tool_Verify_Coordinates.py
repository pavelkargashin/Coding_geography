# coding: utf8
import arcpy, openpyxl, re

# transforming degrees-minutes-seconds like xx.xxxxxx in decimal degrees
def decimating_falseDDD(input):
    result = re.split(r"[\.]", input)
    m = float(result[1][0:2])
    tale = result[1][2:]
    power = len(tale)-2
    s = float(tale)/(10**power)
    value = float(result[0]) + m/60 + s/3600
    return value


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
                    Output.append(decimating_falseDDD(Value))
                    Output_Alternative.append(float(Value))
                # appending key value 1 to the output representing doubts in reading coordinates
                Output.append(1)
                Output_Alternative.append(1)
    # appending key value 0 to the output representing no doubts in reading coordinates
    if len(Output) == 2:
        Output.append(0)
    # don't forget that we are in the southern hemisphere
    if Output[1] > 0:
        Output[1] = Output[1]*(-1)
    if len(Output_Alternative) > 0 and Output_Alternative[1] > 0:
        Output_Alternative[1] = Output_Alternative[1]*(-1)
    return Output, Output_Alternative
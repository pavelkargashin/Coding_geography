import re
import arcpy

def getJenksBreaks(dataList, numClass):
  dataList.sort()
  mat1 = []
  for i in range(0,len(dataList)+1):
    temp = []
    for j in range(0,numClass+1):
      temp.append(0)
    mat1.append(temp)
  mat2 = []
  for i in range(0,len(dataList)+1):
    temp = []
    for j in range(0,numClass+1):
      temp.append(0)
    mat2.append(temp)
  for i in range(1,numClass+1):
    mat1[1][i] = 1
    mat2[1][i] = 0
    for j in range(2,len(dataList)+1):
      mat2[j][i] = float('inf')
  v = 0.0
  for l in range(2,len(dataList)+1):
    s1 = 0.0
    s2 = 0.0
    w = 0.0
    for m in range(1,l+1):
      i3 = l - m + 1
      val = float(dataList[i3-1])
      s2 += val * val
      s1 += val
      w += 1
      v = s2 - (s1 * s1) / w
      i4 = i3 - 1
      if i4 != 0:
        for j in range(2,numClass+1):
          if mat2[l][j] >= (v + mat2[i4][j - 1]):
            mat1[l][j] = i3
            mat2[l][j] = v + mat2[i4][j - 1]
    mat1[l][1] = 1
    mat2[l][1] = v
  k = len(dataList)
  kclass = []
  for i in range(0,numClass+1):
    kclass.append(0)
  kclass[numClass] = float(dataList[len(dataList) - 1])
  countNum = numClass
  while countNum >= 2:#print "rank = " + str(mat1[k][countNum])
    id = int((mat1[k][countNum]) - 2)
    #print "val = " + str(dataList[id])
    kclass[countNum - 1] = dataList[id]
    k = int((mat1[k][countNum] - 1))
    countNum -= 1
  return kclass


def create_fc_environment(inputdataset, environment, outputdataset):
    arcpy.env.workspace = inputdataset
    env_data = outputdataset + '/' + environment
    datalist = arcpy.ListFeatureClasses(environment + '*')
    arcpy.Merge_management(datalist, env_data)
    return env_data


def find_breaks(inputdataset, field):
    templist=[]
    rows = arcpy.da.SearchCursor(env_data, field)
    for row in rows:
        if row[0] != 99999999:
            templist.append(row[0])
        else:
            continue
    print field, max(templist), min(templist)
    myBreaks = getJenksBreaks(templist, 5)
    print sorted(templist)
    print myBreaks
    print "Another data"
    del row
    del rows
    return templist



arcpy.env.overwriteOutput = True
inputdataset = 'C:/PAUL/AAGISTesting/MYGIS/GISEcologyBali.gdb/ThematicData'
outputdataset = 'C:/PAUL/AAGISTesting/MYGIS/GISEcologyBali.gdb/AnalysisData'
environment = "AirSungai"
env_data = create_fc_environment(inputdataset, environment, outputdataset)
field_names = [f.name for f in arcpy.ListFields(env_data,  field_type="Double")]
for field in field_names:
    find_breaks(env_data, field)
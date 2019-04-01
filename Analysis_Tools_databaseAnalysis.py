import re
import arcpy
import configparser
import General_Tools_ConfigFile as GTC
import sys

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
    arcpy.AddMessage(outputdataset)
    env_data = outputdataset + '/' + environment
    datalist = arcpy.ListFeatureClasses(environment + '*')
    arcpy.AddMessage(datalist)
    arcpy.AddMessage(env_data)
    arcpy.Merge_management(datalist, env_data)
    return env_data

def remove_section(configFileName, section_name):
    config = configparser.ConfigParser()
    f = open(configFileName, 'r')
    config.read_file(f)
    if section_name in config.sections():
        print "I have it"
        config.remove_section(section_name)
        f.close()
        with open(configFileName, 'w') as f:
            config.write(f)
    else:
        print "It is no need to delete anything"
    f.close()

def add_section(configFileName, env):
    SectionName = "BreakValues_" + str(env)
    remove_section(configFileName, SectionName)
    config = configparser.ConfigParser()
    with open(configFileName, 'r+') as f:
        config.read(f)
    f.close()
    config.add_section(SectionName)
    with open(configFileName, 'a') as f:
        config.write(f)
    f.close()
    return SectionName

def set_current_config(configFileName, SectionName, Sample, Breaks):
    config = GTC.get_config(configFileName)
    print config
    print "args are"+SectionName, Sample, Breaks
    config.set(SectionName, Sample, str(Breaks))
    with open(configFileName, 'w') as f:
        config.write(f)
    f.close()

def find_breaks(inputdataset, field):
    templist=[]
    rows = arcpy.da.SearchCursor(inputdataset, field)
    for row in rows:
        if row[0] is None:
            continue
        elif row[0] == 99999999:
            continue
        else:
            templist.append(row[0])
    if len(templist) == 0:
        print "empty list"
    else:
        myBreaks = getJenksBreaks(templist, 5)
        del row
        del rows
        return myBreaks
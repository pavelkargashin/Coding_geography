#-*-coding:utf-8-*-
import os, sys
from PyQt4 import QtGui
from functools import partial
import xlwt
import re

# Дополнительные значения
resultList = []
filePath = "C:/PAUL/Science/Python/Files/"

def writeToExcel(inTxt, outExcel):
    wbk=xlwt.Workbook()
    sheet = wbk.add_sheet('NewData')
    row = 0
    f=open(inTxt)
    for line in f:
        # separate fields by commas
        # L = line.strip()
        l = list(line)
        sheet.write(row, 0, l)
    wbk.save(outExcel)


def checkInput(val):
    count =0
    for i in val:
        if i==',' or i=='.':
            count+=1
        else:
            continue
    print count
    if count==0 or count ==1:
        try:
            res=re.sub(r'[,.]', '.',val)
            res = float(res)
        except:
            print('There is something wrong with your data')
            res='Bad Data'
    print res, type(res)
    return res



class myProgramm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(myProgramm, self).__init__()
        self.initUI()

    def initUI(self):

        # Создание объектов формы
        introduction = QtGui.QLabel('Enter your data below!', self)
        at_Year = QtGui.QLabel('Year', self)
        at_RiverName = QtGui.QLabel('River name', self)
        at_NameLocation = QtGui.QLabel('Name Location', self)
        at_KoordLS = QtGui.QLabel('Koordinat LS', self)
        at_KoordBT = QtGui.QLabel('Koordinat BT', self)
        at_Stage = QtGui.QLabel('Stage', self)
        at_Time = QtGui.QLabel('Time', self)

        self.at_Year_Edit = QtGui.QLineEdit(self)
        self.at_RiverName_Edit = QtGui.QLineEdit(self)
        self.at_NameLocation_Edit = QtGui.QLineEdit(self)
        self.at_KoordLS_Edit = QtGui.QLineEdit(self)
        self.at_KoordBT_Edit = QtGui.QLineEdit(self)
        self.at_Stage_Edit = QtGui.QLineEdit(self)
        self.at_Time_Edit = QtGui.QLineEdit(self)

        self.statusLbl = QtGui.QLabel('Current status of processing', self)
        # Button to write data in the list while checking it
        wrtBut = QtGui.QPushButton('Write', self)
        wrtBut.clicked.connect(partial(self.wrtButClc))
        newBut = QtGui.QPushButton('New data', self)
        newBut.clicked.connect(partial(self.clrData))
        clsBut = QtGui.QPushButton('Close', self)
        clsBut.clicked.connect(self.clsApp)
        # Button to set information to txt file
        setBut = QtGui.QPushButton('Set to file', self)
        setBut.clicked.connect(self.setData)

        # Создание сетки
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        #Размещение объектов
        grid.addWidget(introduction, 1, 0)
        grid.addWidget(at_Year, 2, 0)
        grid.addWidget(self.at_Year_Edit, 2, 1)
        grid.addWidget(at_RiverName, 3, 0)
        grid.addWidget(self.at_RiverName_Edit, 3, 1)
        grid.addWidget(at_NameLocation, 4, 0)
        grid.addWidget(self.at_NameLocation_Edit, 4, 1)
        grid.addWidget(at_KoordLS, 5, 0)
        grid.addWidget(self.at_KoordLS_Edit, 5, 1)
        grid.addWidget(at_KoordBT, 6, 0)
        grid.addWidget(self.at_KoordBT_Edit, 6, 1)
        grid.addWidget(at_Stage, 7, 0)
        grid.addWidget(self.at_Stage_Edit, 7, 1)
        grid.addWidget(at_Time, 8, 0)
        grid.addWidget(self.at_Time_Edit, 8, 1)

        grid.addWidget(setBut, 2, 2)
        grid.addWidget(newBut, 4, 2)
        grid.addWidget(wrtBut, 3, 2)
        grid.addWidget(clsBut, 5, 2)
        # grid.addWidget(self.statusLbl, 6, 0, 6, 1)


        # Block of new widgets to set and further to place correct
        at_Temperature = QtGui.QLabel('Temperature', self)
        self.at_Temperature_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Temperature, 9, 0)
        grid.addWidget(self.at_Temperature_Edit, 9, 1)

        at_pH = QtGui.QLabel('pH', self)
        self.at_pH_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_pH, 10, 0)
        grid.addWidget(self.at_pH_Edit, 10, 1)

        at_DHL_MosCM = QtGui.QLabel('DHL_MosCM', self)
        self.at_DHL_MosCM_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_DHL_MosCM, 11, 0)
        grid.addWidget(self.at_DHL_MosCM_Edit, 11, 1)

        at_TDSmgl = QtGui.QLabel('TDSmgl', self)
        self.at_TDSmgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_TDSmgl, 12, 0)
        grid.addWidget(self.at_TDSmgl_Edit, 12, 1)

        at_TSSmgl = QtGui.QLabel('TSSmgl', self)
        self.at_TSSmgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_TSSmgl, 13, 0)
        grid.addWidget(self.at_TSSmgl_Edit, 13, 1)

        at_DOmgl = QtGui.QLabel('DOmgl', self)
        self.at_DOmgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_DOmgl, 14, 0)
        grid.addWidget(self.at_DOmgl_Edit, 14, 1)

        at_BODmgl = QtGui.QLabel('BODmgl', self)
        self.at_BODmgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_BODmgl, 15, 0)
        grid.addWidget(self.at_BODmgl_Edit, 15, 1)

        at_CODmgl = QtGui.QLabel('CODmgl', self)
        self.at_CODmgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_CODmgl, 16, 0)
        grid.addWidget(self.at_CODmgl_Edit, 16, 1)

        at_NO2mgl = QtGui.QLabel('NO2mgl', self)
        self.at_NO2mgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_NO2mgl, 17, 0)
        grid.addWidget(self.at_NO2mgl_Edit, 17, 1)

        at_NO3mgl = QtGui.QLabel('NO3mgl', self)
        self.at_NO3mgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_NO3mgl, 18, 0)
        grid.addWidget(self.at_NO3mgl_Edit, 18, 1)

        at_NH3mgl = QtGui.QLabel('NH3mgl', self)
        self.at_NH3mgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_NH3mgl, 19, 0)
        grid.addWidget(self.at_NH3mgl_Edit, 19, 1)

        at_FreeChlorine_mgl = QtGui.QLabel('FreeChlorine_mgl', self)
        self.at_FreeChlorine_mgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_FreeChlorine_mgl, 20, 0)
        grid.addWidget(self.at_FreeChlorine_mgl_Edit, 20, 1)

        at_TotalP_mgl = QtGui.QLabel('TotalP_mgl', self)
        self.at_TotalP_mgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_TotalP_mgl, 21, 0)
        grid.addWidget(self.at_TotalP_mgl_Edit, 21, 1)

        at_Phenol_mgl = QtGui.QLabel('Phenol_mgl', self)
        self.at_Phenol_mgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Phenol_mgl, 22, 0)
        grid.addWidget(self.at_Phenol_mgl_Edit, 22, 1)

        at_OilAndFat_mgl = QtGui.QLabel('OilAndFat_mgl', self)
        self.at_OilAndFat_mgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_OilAndFat_mgl, 23, 0)
        grid.addWidget(self.at_OilAndFat_mgl_Edit, 23, 1)

        at_Detergent_mgl = QtGui.QLabel('Detergent_mgl', self)
        self.at_Detergent_mgl_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Detergent_mgl, 24, 0)
        grid.addWidget(self.at_Detergent_mgl_Edit, 24, 1)

        at_FecalColiform = QtGui.QLabel('FecalColiform', self)
        self.at_FecalColiform_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_FecalColiform, 25, 0)
        grid.addWidget(self.at_FecalColiform_Edit, 25, 1)

        at_TotalColiform = QtGui.QLabel('TotalColiform', self)
        self.at_TotalColiform_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_TotalColiform, 26, 0)
        grid.addWidget(self.at_TotalColiform_Edit, 26, 1)

        at_Cyanide = QtGui.QLabel('Cyanide', self)
        self.at_Cyanide_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Cyanide, 27, 0)
        grid.addWidget(self.at_Cyanide_Edit, 27, 1)

        at_Sulfide = QtGui.QLabel('Sulfide', self)
        self.at_Sulfide_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Sulfide, 28, 0)
        grid.addWidget(self.at_Sulfide_Edit, 28, 1)

        at_Turbidity_NTU = QtGui.QLabel('Turbidity_NTU', self)
        self.at_Turbidity_NTU_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Turbidity_NTU, 29, 0)
        grid.addWidget(self.at_Turbidity_NTU_Edit, 29, 1)

        at_Cd_mgL = QtGui.QLabel('Cd_mgL', self)
        self.at_Cd_mgL_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Cd_mgL, 30, 0)
        grid.addWidget(self.at_Cd_mgL_Edit, 30, 1)

        at_Fe_mgL = QtGui.QLabel('Fe_mgL', self)
        self.at_Fe_mgL_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Fe_mgL, 31, 0)
        grid.addWidget(self.at_Fe_mgL_Edit, 31, 1)

        at_PO4_mgL = QtGui.QLabel('PO4_mgL', self)
        self.at_PO4_mgL_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_PO4_mgL, 32, 0)
        grid.addWidget(self.at_PO4_mgL_Edit, 32, 1)

        at_SO4_mgL = QtGui.QLabel('SO4_mgL', self)
        self.at_SO4_mgL_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_SO4_mgL, 33, 0)
        grid.addWidget(self.at_SO4_mgL_Edit, 33, 1)

        at_Pb_mgL = QtGui.QLabel('Pb_mgL', self)
        self.at_Pb_mgL_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Pb_mgL, 34, 0)
        grid.addWidget(self.at_Pb_mgL_Edit, 34, 1)

        at_Mn_mgL = QtGui.QLabel('Mn_mgL', self)
        self.at_Mn_mgL_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Mn_mgL, 35, 0)
        grid.addWidget(self.at_Mn_mgL_Edit, 35, 1)

        at_Zn_mgL = QtGui.QLabel('Zn_mgL', self)
        self.at_Zn_mgL_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Zn_mgL, 36, 0)
        grid.addWidget(self.at_Zn_mgL_Edit, 36, 1)

        at_Cr_mgL = QtGui.QLabel('Cr_mgL', self)
        self.at_Cr_mgL_Edit = QtGui.QLineEdit(self)
        grid.addWidget(at_Cr_mgL, 37, 0)
        grid.addWidget(self.at_Cr_mgL_Edit, 37, 1)









        self.setLayout(grid)
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle("My data input")
        self.show()

    def wrtButClc(self):
        print('Hello world!')
        myList=[]
        tempList = []
        myList.append(str(self.at_Year_Edit.text()))
        myList.append(str(self.at_RiverName_Edit.text()))
        myList.append(str(self.at_NameLocation_Edit.text()))
        for i in range(0, 3, 1):
            tempVal = myList[i]
            if len(tempVal)==0:
                tempVal='Nodata'
            if i==1:
                try:
                    tempVal=float(tempVal)
                except:
                    tempVal='Bad Value'
            tempList.append(tempVal)
        print(tempList)
        mes=''
        for i in tempList:
            mes = mes+str(i)+'-'
        self.statusLbl.setText(mes)
        resultList.append(tempList)
        print resultList
        return resultList

    def clrData(self):
        self.at_Year_Edit.setText('')
        self.at_RiverName_Edit.setText('')
        self.at_NameLocation_Edit.setText('')

    def clsApp(self):
        self.close()

    def setData(self):
        for item in resultList:
            data=str(item).strip('[]')
            with open(filePath + "newData.txt", "a") as myFile:
                myFile.write(data+'\n')

def main():
    app = QtGui.QApplication(sys.argv)
    myApp = myProgramm()
    myApp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


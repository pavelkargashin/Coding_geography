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
        at1 = QtGui.QLabel('Attr1', self)
        at2 = QtGui.QLabel('Attr2', self)
        at3 = QtGui.QLabel('Attr3', self)
        self.at1Edit = QtGui.QLineEdit(self)
        self.at2Edit = QtGui.QLineEdit(self)
        self.at3Edit = QtGui.QLineEdit(self)
        self.statusLbl = QtGui.QLabel('Current status of processing', self)
        wrtBut = QtGui.QPushButton('Write', self)
        wrtBut.clicked.connect(partial(self.wrtButClc))
        newBut = QtGui.QPushButton('New data', self)
        newBut.clicked.connect(partial(self.clrData))
        clsBut = QtGui.QPushButton('Close', self)
        clsBut.clicked.connect(self.clsApp)
        setBut = QtGui.QPushButton('Set to file', self)
        setBut.clicked.connect(self.setData)

        # Создание сетки
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        #Размещение объектов
        grid.addWidget(introduction, 1, 0)
        grid.addWidget(at1, 2, 0)
        grid.addWidget(self.at1Edit, 2, 1)
        grid.addWidget(at2, 3, 0)
        grid.addWidget(self.at2Edit, 3, 1)
        grid.addWidget(at3, 4, 0)
        grid.addWidget(self.at3Edit, 4, 1)
        grid.addWidget(setBut, 2, 2)
        grid.addWidget(newBut, 4, 2)
        grid.addWidget(wrtBut, 3, 2)
        grid.addWidget(clsBut, 5, 2)
        grid.addWidget(self.statusLbl, 6, 0, 6, 1)

        self.setLayout(grid)
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle("My data input")
        self.show()

    def wrtButClc(self):
        print('Hello world!')
        myList=[]
        tempList = []
        myList.append(str(self.at1Edit.text()))
        myList.append(str(self.at2Edit.text()))
        myList.append(str(self.at3Edit.text()))
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
        self.at1Edit.setText('')
        self.at2Edit.setText('')
        self.at3Edit.setText('')

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


#!/usr/bin
# -*-coding:utf-8-*-
import sys
from PyQt4 import QtCore, QtGui
from openpyxl import *

data = ['Year',
        'Stage',
        'Environment',
        'Object name',
        'Location',
        'Latitude',
        'Longitude']

class InputWindow(QtGui.QWidget):



    def __init__(self, parent = None):
        super(InputWindow, self).__init__(parent)
        self.build()




    def build(self):
        self.widglist = []

        gr = QtGui.QGridLayout()

        counter = 0
        for item in data:
            widname = 'lbl' + str(item)
            widname2 = 'te' + str(item)
            self.widname = QtGui.QLabel(str(item), self)
            self.widname2 = QtGui.QTextEdit()
            self.widname2.setFixedSize(100, 30)
            self.widglist.append(self.widname2)
            gr.addWidget(self.widname, counter, 0)
            gr.addWidget(self.widname2, counter, 1)
            counter += 1

        self.checkBut = QtGui.QPushButton('Verify entered data', self)
        gr.addWidget(self.checkBut, 0, 2)
        self.checkBut.clicked.connect(self.verifyData)

        closeBut = QtGui.QPushButton('Close', self)
        closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
        gr.addWidget(closeBut, 6, 2)

        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 250)
        self.setWindowTitle('Enter yor data')
        self.show()

    def verifyData(self):
            values = []
            print 'Data verification!'
            for item in self.widglist:
                mytext = str(item.toPlainText())
                values.append(mytext)
            oneset = dict(zip(data, values))

            print oneset
            return

if __name__ == '__main__':
    myApp = QtGui.QApplication(sys.argv)
    myProg = InputWindow()
    myProg.show()
    sys.exit(myApp.exec_())
#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
import ProjectManagement
from PyQt4 import QtGui, QtCore
home = os.getenv("HOME")
import parameters_test
import General_Tools_ConfigFile as GTC


class MainWindow(QtGui.QWidget):
    configFile = "No File"



    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.build()

    def build(self):


        gr = QtGui.QGridLayout()


        self.btn1 = QtGui.QPushButton('Select Configuration File', self)
        gr.addWidget(self.btn1, 1, 0)
        self.btn1.clicked.connect(self.showSelector)

        # self.btn2 = QtGui.QPushButton('Set data', self)
        # gr.addWidget(self.btn2, 2, 0)
        # self.btn2.clicked.connect(self.setPath)

        btn3 = QtGui.QPushButton('Run create project', self)
        btn3.clicked.connect(self.createProject)
        gr.addWidget(btn3, 4, 4)

        closeBut = QtGui.QPushButton('Close', self)
        closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
        gr.addWidget(closeBut, 5, 4)


        self.lbl1 = QtGui.QLabel(MainWindow.configFile)
        gr.addWidget(self.lbl1, 1, 1)
        # self.lbl2 =QtGui.QLabel(MainWindow.configFile, self)
        # gr.addWidget(self.lbl2, 3, 0, 3, 2)

        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Project Deployment')
        self.show()


    # def showDialog(self):
    #     newtext, ok = QtGui.QInputDialog.getText(None, "Input", "Enter the name of the Project (in English)")
    #     if ok:
    #         self.lbl1.setText(str(newtext))
    #     MainWindow.projectName = str(newtext)
    #     return MainWindow.projectName

    def showSelector(self):
        conffilename = QtGui.QFileDialog.getOpenFileName(self, 'Select config file')
        self.lbl1.setText(conffilename)
        MainWindow.configFile = conffilename
        print MainWindow.configFile
        return MainWindow.configFile

    # def setPath(self):
    #     MainWindow.projectFolder = MainWindow.projectPath + MainWindow.projectName
    #     tempdata = parameters_test.update_filepath(MainWindow.projectFolder)
    #     self.lbl2.setText(tempdata)
    #     MainWindow.projectFolder = tempdata
    #     return tempdata

    def createProject(self):

        print "The file is: ", MainWindow.configFile
        inputdata = GTC.get_setting(str(MainWindow.configFile), section='Paths', setting='projectfolder')
        print inputdata
        # ProjectManagement.main_2(inputdata)



if __name__ == '__main__':
    # Создание окна
    # pyhtonProjectPath = 'C:/PAUL/Science/Coding_geography/'

    myApp = QtGui.QApplication(sys.argv)
    myProg = MainWindow()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())

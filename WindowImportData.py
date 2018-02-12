#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
import shutil
from PyQt4 import QtGui, QtCore
home = os.getenv("HOME")
import ProjectManagement
import parameters_test





class MainWindow(QtGui.QWidget):
    ProjectFolder = "No Project"
    ConfigFileName = ProjectFolder+ ProjectManagement.configFileName
    BaseMapFolder = 'NoFolder'

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.build()

    def build(self):

        gr = QtGui.QGridLayout()

        self.btn4 = QtGui.QPushButton('Set the project', self)
        gr.addWidget(self.btn4, 5, 0)
        self.btn4.clicked.connect(self.runImport)

        self.btn3 = QtGui.QPushButton('Set the project', self)
        gr.addWidget(self.btn3, 0, 0)
        self.btn3.clicked.connect(self.showSelector3)

        self.lbl3 = QtGui.QLabel(MainWindow.ProjectFolder, self)
        gr.addWidget(self.lbl3, 0, 1)



        self.btn1 = QtGui.QPushButton('Select *.xslx file', self)
        gr.addWidget(self.btn1, 1, 0)
        self.btn1.clicked.connect(self.showSelector1)

        self.btn2 = QtGui.QPushButton('Select path to basemap data (*.shp)', self)
        gr.addWidget(self.btn2, 2, 0)
        self.btn2.clicked.connect(self.showSelector2)

        self.lbl1 = QtGui.QLabel('ThematicFileName', self)
        gr.addWidget(self.lbl1, 1, 1)

        self.lbl2 = QtGui.QLabel('Basemap Data', self)
        gr.addWidget(self.lbl2, 2, 1)


        self.lbl4 = QtGui.QLabel('IMPORT TO DATABASE', self)
        gr.addWidget(self.lbl4, 4,0)

        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Collect Data')
        self.show()

    def showSelector1(self):
        selectedFileName = QtGui.QFileDialog.getOpenFileName(self, "Select *.xlsx with your data", self.lbl1.text())
        print selectedFileName
        thematicFileName = str(selectedFileName)
        thematicFileName.replace('\\', '/')
        pathToCopy = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'InputData')
        dstFileName = pathToCopy+os.path.basename(thematicFileName)
        print dstFileName
        shutil.copy(thematicFileName, dstFileName)
        return thematicFileName

    def showSelector2(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Set folder with Basemap data", self.lbl2.text(), options)
        if foldername:
            self.lbl2.setText(foldername)
        tempfolder = str(foldername)
        tempfolder.replace('\\', '/')
        MainWindow.BaseMapFolder = tempfolder + '/'
        pathToCopy = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'InputData')
        for item in os.listdir(MainWindow.BaseMapFolder):
            print item
            shutil.copy(MainWindow.BaseMapFolder+item, pathToCopy+item)

        return MainWindow.BaseMapFolder

    def showSelector3(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Path to project", self.lbl3.text(), options)
        if foldername:
            self.lbl3.setText(foldername)
        tempfolder = str(foldername)
        tempfolder.replace('\\', '/')
        MainWindow.ProjectFolder = tempfolder + '/'
        return MainWindow.ProjectFolder


    def runImport(self):
        return


if __name__ == '__main__':
    # Создание окна
    # pyhtonProjectPath = 'C:/PAUL/Science/Coding_geography/'

    myApp = QtGui.QApplication(sys.argv)
    myProg = MainWindow()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())
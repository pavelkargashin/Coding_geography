#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
import shutil
from PyQt4 import QtGui, QtCore
home = os.getenv("HOME")
import ProjectManagement
import parameters_test
import ImportBasemap
import importProcessing
import databaseProcessing


class MainWindow(QtGui.QWidget):
    ProjectFolder = "No Project"
    ConfigFileName = ProjectManagement.configFileName
    BaseMapFolder = 'NoFolder'

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.build()

    def build(self):

        gr = QtGui.QGridLayout()

        self.ImportBut = QtGui.QPushButton('Run Import!', self)
        gr.addWidget(self.ImportBut, 5, 0)
        self.ImportBut.clicked.connect(self.runImport)

        self.ProjectSetBut = QtGui.QPushButton('Set the project', self)
        gr.addWidget(self.ProjectSetBut, 0, 0)
        self.ProjectSetBut.clicked.connect(self.SetProject)

        self.ProjectNameLbl = QtGui.QLabel(MainWindow.ProjectFolder, self)
        gr.addWidget(self.ProjectNameLbl, 0, 1)

        self.ThematicBut = QtGui.QPushButton('Select *.xslx file', self)
        gr.addWidget(self.ThematicBut, 1, 0)
        self.ThematicBut.clicked.connect(self.SelectThematic)

        self.BasemapBut = QtGui.QPushButton('Select path to basemap data (*.shp)', self)
        gr.addWidget(self.BasemapBut, 2, 0)
        self.BasemapBut.clicked.connect(self.SelectBasemap)

        self.ThematicLbl = QtGui.QLabel('ThematicFileName', self)
        gr.addWidget(self.ThematicLbl, 1, 1)

        self.BasemapLbl = QtGui.QLabel('Basemap Data', self)
        gr.addWidget(self.BasemapLbl, 2, 1)


        self.lbl4 = QtGui.QLabel('IMPORT TO DATABASE', self)
        gr.addWidget(self.lbl4, 4,0)

        closeBut = QtGui.QPushButton('Close', self)
        closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
        gr.addWidget(closeBut, 5, 4)


        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Collect Data')
        self.show()

    def SelectThematic(self):
        selectedFileName = QtGui.QFileDialog.getOpenFileName(self, "Select *.xlsx with your data", self.ThematicLbl.text())
        self.ThematicLbl.setText(selectedFileName)
        thematicFileName = parameters_test.update_filepath(selectedFileName)
        thematicFileName.replace('\\', '/')
        pathToCopy = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'InputData')
        dstFileName = pathToCopy+os.path.basename(thematicFileName)
        shutil.copy(thematicFileName, dstFileName)
        print 'Thematic data has been copied!'
        return thematicFileName

    def SelectBasemap(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Set folder with Basemap data", self.BasemapLbl.text(), options)
        if foldername:
            self.BasemapLbl.setText(parameters_test.update_filepath(foldername))

        MainWindow.BaseMapFolder = parameters_test.update_filepath(foldername) + '/'
        pathToCopy = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'InputData')
        for item in os.listdir(MainWindow.BaseMapFolder):
            shutil.copy(MainWindow.BaseMapFolder+item, pathToCopy+item)
        print 'Shapefiles has been copied!'

        return MainWindow.BaseMapFolder

    def SetProject(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Path to project", self.ProjectNameLbl.text(), options)
        if foldername:
            self.ProjectNameLbl.setText(parameters_test.update_filepath(foldername))
        MainWindow.ProjectFolder = parameters_test.update_filepath(foldername) + '/'
        return MainWindow.ProjectFolder


    def runImport(self):
        print MainWindow.ProjectFolder
        ImportBasemap.main(MainWindow.ProjectFolder, ProjectManagement.configFileName)
        inputFolder = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'InputData')
        # Convert thematic data to shapefiles
        excelName = self.ThematicLbl.text()
        dstFileName = os.path.basename(str(excelName))
        outputFolder = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'TempData')
        importProcessing.main(inputFolder, dstFileName, "Kualitas Air", outputFolder)
        # Import data to geodatabase
        inputfolder_shp = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'TempData')
        envDatabase = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'ProjectFolder')\
                      +parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'GISDataName')+'.gdb'
        ThematicDataset = envDatabase+'/' + parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'Paths', 'ThematicDatasetName')
        fieldname = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'ImportParameters', 'fieldname')
        fieldname_2 = parameters_test.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, 'ImportParameters', 'fieldname_2')
        databaseProcessing.main(inputfolder_shp, envDatabase,ThematicDataset, fieldname, fieldname_2)
        return


if __name__ == '__main__':
    # Создание окна
    # pyhtonProjectPath = 'C:/PAUL/Science/Coding_geography/'

    myApp = QtGui.QApplication(sys.argv)
    myProg = MainWindow()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())
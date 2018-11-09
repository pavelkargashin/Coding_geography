#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
import shutil
from PyQt4 import QtGui, QtCore
import ProjectManagement
import General_Tools_ConfigFile as GTC
import Create_Exec_ImportBasemap
import importProcessing
import databaseProcessing

home = os.getenv("HOME")

Paths = 'Paths'

class MainWindow(QtGui.QWidget):
    ConfigFileName = "CONFIGURATION"
    ProjectFolder = "No Project"
    BaseMapFolder = 'NoFolder'

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.build()

    def build(self):

        gr = QtGui.QGridLayout()

        self.ImportBut = QtGui.QPushButton('Run Import!', self)
        gr.addWidget(self.ImportBut, 5, 0)
        self.ImportBut.clicked.connect(self.runImport)

        self.ProjectSetBut = QtGui.QPushButton('Show project path', self)
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
        thematicFileName = GTC.update_filepath(selectedFileName)
        thematicFileName.replace('\\', '/')
        pathToCopy = GTC.get_setting(MainWindow.ProjectFolder, ProjectManagement.configFileName, Paths, 'InputData')
        dstFileName = pathToCopy+os.path.basename(thematicFileName)
        shutil.copy(thematicFileName, dstFileName)
        print 'Thematic data has been copied!'
        return thematicFileName

    def SelectBasemap(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Set folder with Basemap data", self.BasemapLbl.text(), options)
        if foldername:
            self.BasemapLbl.setText(GTC.update_filepath(foldername))

        MainWindow.BaseMapFolder = GTC.update_filepath(foldername) + '/'
        pathToCopy = GTC.get_setting(MainWindow.ConfigFileName, Paths, 'inputdata')
        for item in os.listdir(MainWindow.BaseMapFolder):
            shutil.copy(MainWindow.BaseMapFolder+item, pathToCopy+item)
        print 'Shapefiles have been copied!'

        return MainWindow.BaseMapFolder

    def SetProject(self):
        foldername = GTC.get_setting(str(MainWindow.ConfigFileName), Paths, 'projectfolder')
        self.ProjectNameLbl.setText(foldername)
        MainWindow.ProjectFolder = foldername
        return MainWindow.ProjectFolder


    def runImport(self):
        print 'initial value of project folder is ', MainWindow.ProjectFolder
        Create_Exec_ImportBasemap.main(MainWindow.ConfigFileName)
        sys.exit()
        inputFolder = GTC.get_setting(MainWindow.ConfigFileName, Paths, 'InputData')
        # Convert thematic data to shapefiles
        excelName = self.ThematicLbl.text()
        dstFileName = os.path.basename(str(excelName))
        outputFolder = GTC.get_setting(MainWindow.ConfigFileName, Paths, 'tempdata')
        importProcessing.main(inputFolder, dstFileName, "Kualitas Air", outputFolder)
        # Import data to geodatabase
        inputfolder_shp = GTC.get_setting(MainWindow.ConfigFileName, Paths, 'tempdata')
        envDatabase = GTC.get_setting(MainWindow.ConfigFileName, Paths, 'projectfolder')\
                      +GTC.get_setting(MainWindow.ConfigFileName, Paths, 'gisdataname')+'.gdb'
        ThematicDataset = envDatabase+'/' + GTC.get_setting(MainWindow.ConfigFileName, Paths, 'thematicdatasetname')
        fieldname = GTC.get_setting(MainWindow.ConfigFileName, 'ImportParameters', 'fieldname')
        fieldname_2 = GTC.get_setting(MainWindow.ConfigFileName, 'ImportParameters', 'fieldname_2')
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
#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
import shutil
from PyQt4 import QtGui, QtCore
home = os.getenv("HOME")
import ProjectManagement
import parameters_test
import CheckDBStatistics

class MainWindow(QtGui.QWidget):
    ProjectFolder = "C:/PAUL/AAGISTesting/MYGIS/"
    ConfigFileName = ProjectManagement.configFileName
    GIS = ProjectFolder + parameters_test.get_setting(ProjectFolder, ConfigFileName, 'Paths', 'GISDataName') + '.gdb/'
    ThematicDataset = GIS+parameters_test.get_setting(ProjectFolder, ConfigFileName, 'Paths', 'ThematicDatasetName')+'/'

    listfc = CheckDBStatistics.create_listfc(ThematicDataset, "*")
    envs = CheckDBStatistics.create_stat(listfc)[0]
    years = CheckDBStatistics.create_stat(listfc)[1]
    stages = CheckDBStatistics.create_stat(listfc)[2]
    print envs

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.build()

    def build(self):
        gr = QtGui.QGridLayout()

        self.ProjectSetBut = QtGui.QPushButton('Set the project', self)
        gr.addWidget(self.ProjectSetBut, 0, 0)
        self.ProjectSetBut.clicked.connect(self.SetProject)

        self.ProjectNameLbl = QtGui.QLabel(MainWindow.ProjectFolder, self)
        gr.addWidget(self.ProjectNameLbl, 0, 1)


        self.EnvCB = QtGui.QComboBox(self)
        for item in MainWindow.envs:
            self.EnvCB.addItem(item)
        self.EnvCB.currentIndexChanged.connect(self.selectionchange)

        gr.addWidget(self.EnvCB, 1 ,0)


        self.YearCB = QtGui.QComboBox(self)
        for item in MainWindow.years:
            self.YearCB.addItem(item)
        gr.addWidget(self.YearCB, 1, 1)

        self.StageCB = QtGui.QComboBox(self)
        for item in MainWindow.stages:
            self.StageCB.addItem(item)
        gr.addWidget(self.StageCB, 1, 2)

        self.CheckPB = QtGui.QPushButton("Check data if it exists in database")
        self.CheckPB.clicked.connect(self.check_data)
        gr.addWidget(self.CheckPB, 2,0)

        self.fcLbl = QtGui.QLabel("Data for mapping", self)
        gr.addWidget(self.fcLbl, 2, 1)





        closeBut = QtGui.QPushButton('Close', self)
        closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
        gr.addWidget(closeBut, 5, 4)


        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Collect Data')
        self.show()

    def selectionchange(self, i):
         self.EnvCB.currentText()


    def SetProject(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Path to project", self.ProjectNameLbl.text(), options)
        if foldername:
            self.ProjectNameLbl.setText(parameters_test.update_filepath(foldername))
        MainWindow.ProjectFolder = parameters_test.update_filepath(foldername) + '/'
        ProjectSet = parameters_test.update_filepath(foldername) + '/'
        GIS = ProjectSet + parameters_test.get_setting(ProjectSet, MainWindow.ConfigFileName, 'Paths',
                                                          'GISDataName') + '.gdb/'
        ThematicDataset = GIS + parameters_test.get_setting(ProjectSet, MainWindow.ConfigFileName, 'Paths',
                                                            'ThematicDatasetName') + '/'

        return MainWindow.ProjectFolder, MainWindow.ThematicDataset

    def check_data(self):
        data2process = self.EnvCB.currentText()+'_'+self.YearCB.currentText()+'_'+self.StageCB.currentText()
        if data2process in MainWindow.listfc:
            self.fcLbl.setText("data to process: "+ data2process)
        else:
            self.fcLbl.setText("select something else")

        return

if __name__ == '__main__':
    # Создание окна
    # pyhtonProjectPath = 'C:/PAUL/Science/Coding_geography/'

    myApp = QtGui.QApplication(sys.argv)
    myProg = MainWindow()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())
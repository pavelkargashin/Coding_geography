#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
from PyQt4 import QtGui, QtCore
import arcpy
home = os.getenv("HOME")
import ProjectManagement
import parameters_test
import CheckDBStatistics



class overall_params():
    glProjectFolder = 'None'
    inputdata = []
    listFC = []

class FirstWindow(QtGui.QWidget):
    ConfigFileName = ProjectManagement.configFileName

    def __init__(self, parent = None):
        super(FirstWindow, self).__init__(parent)
        self.build()
    def build(self):
        gr = QtGui.QGridLayout()

        self.ProjectSetBut = QtGui.QPushButton('Set the project', self)
        gr.addWidget(self.ProjectSetBut, 0, 0)
        self.ProjectSetBut.clicked.connect(self.SetProjectNew)

        self.ProjectNameLbl = QtGui.QLabel(overall_params.glProjectFolder, self)
        gr.addWidget(self.ProjectNameLbl, 0, 1)


        self.WorkWithProjectBut = QtGui.QPushButton('Start work', self)
        gr.addWidget(self.WorkWithProjectBut, 4, 4)
        self.WorkWithProjectBut.clicked.connect(self.OpenAnotherWindow)
        closeBut = QtGui.QPushButton('Close', self)
        closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
        gr.addWidget(closeBut, 5, 4)

        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Collect Data')
        self.show()

    def SetProjectNew(self):
            options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
            foldername = QtGui.QFileDialog.getExistingDirectory(self, "Path to project", self.ProjectNameLbl.text(),
                                                                options)
            if foldername:
                self.ProjectNameLbl.setText(parameters_test.update_filepath(foldername))
                self.ProjectFolder = parameters_test.update_filepath(foldername)+'/'
                overall_params.glProjectFolder = parameters_test.update_filepath(foldername)+'/'
                print 'After assigning',overall_params.glProjectFolder
            return overall_params.glProjectFolder

    def OpenAnotherWindow(self):
        GIS = self.ProjectFolder + parameters_test.get_setting(self.ProjectFolder, self.ConfigFileName, 'Paths',
                                                          'GISDataName') + '.gdb/'
        ThematicDataset = GIS + parameters_test.get_setting(self.ProjectFolder, self.ConfigFileName, 'Paths',
                                                            'ThematicDatasetName') + '/'
        print ThematicDataset+'---------'+overall_params.glProjectFolder
        listfc = CheckDBStatistics.create_listfc(ThematicDataset, "*")
        overall_params.listFC = listfc
        print 'we will work with it', overall_params.listFC
        envs = CheckDBStatistics.create_stat(listfc)[0]
        overall_params.inputdata.append(envs)
        years = CheckDBStatistics.create_stat(listfc)[1]
        overall_params.inputdata.append(years)
        stages = CheckDBStatistics.create_stat(listfc)[2]
        overall_params.inputdata.append(stages)
        secondWindow = MainWindow()
        self.secondWindow.show()


class MainWindow(QtGui.QWidget):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.build()

    def build(self):
        gr = QtGui.QGridLayout()
        self.ProjectNameLbl = QtGui.QLabel(overall_params.glProjectFolder, self)
        gr.addWidget(self.ProjectNameLbl, 0, 1)

        self.EnvCB = QtGui.QComboBox(self)
        for item in overall_params.inputdata[0]:
            self.EnvCB.addItem(item)
        # self.EnvCB.currentIndexChanged.connect(self.selectionchange)
        gr.addWidget(self.EnvCB, 1 ,0)


        self.YearCB = QtGui.QComboBox(self)
        for item in overall_params.inputdata[1]:
            self.YearCB.addItem(item)
        gr.addWidget(self.YearCB, 1, 1)

        self.StageCB = QtGui.QComboBox(self)
        for item in overall_params.inputdata[2]:
            self.StageCB.addItem(item)
        gr.addWidget(self.StageCB, 1, 2)

        self.CheckPB = QtGui.QPushButton("Check data if it exists in database")
        self.CheckPB.clicked.connect(self.check_data)
        gr.addWidget(self.CheckPB, 2,0)

        self.fcLbl = QtGui.QLabel("Data for mapping", self)
        gr.addWidget(self.fcLbl, 2, 1)

        self.MapPB = QtGui.QPushButton("Create map", self)
        self.MapPB.clicked.connect(self.create_map)
        gr.addWidget(self.MapPB, 3, 0)


        closeBut = QtGui.QPushButton('Close', self)
        closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
        gr.addWidget(closeBut, 5, 4)


        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Collect Data')
        self.show()

    def selectionchange(self, i):
         self.EnvCB.currentText()


    def create_map(self):
        path2MXD = parameters_test.get_setting(overall_params.glProjectFolder, ProjectManagement.configFileName, 'Paths',
                                                          'mxdName')
        myMXD = arcpy.mapping.MapDocument(path2MXD)


    def check_data(self):
        data2process = self.EnvCB.currentText()+'_'+self.YearCB.currentText()+'_'+self.StageCB.currentText()
        print data2process
        if data2process in overall_params.listFC:
            self.fcLbl.setText("data to process: "+ data2process)
        else:
            self.fcLbl.setText("select something else")

        return

if __name__ == '__main__':
    # Создание окна

    myApp = QtGui.QApplication(sys.argv)
    myProg = FirstWindow()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())
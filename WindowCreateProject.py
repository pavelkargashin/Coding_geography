#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
import ProjectManagement
from PyQt4 import QtGui, QtCore
home = os.getenv("HOME")
import parameters_test


class MainWindow(QtGui.QWidget):
    projectPath = "NoFolder"
    projectName = "NoName"
    projectFolder = projectPath + '/' + projectName
    projectFolder.replace('\\', '/')

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.build()

    def build(self):

        gr = QtGui.QGridLayout()

        self.btn1 = QtGui.QPushButton('Set Name', self)
        gr.addWidget(self.btn1, 0,0)
        self.btn1.clicked.connect(self.showDialog)

        self.btn2 = QtGui.QPushButton('Select path', self)
        gr.addWidget(self.btn2, 1, 0)
        self.btn2.clicked.connect(self.showSelector)

        self.btn3 = QtGui.QPushButton('Set data', self)
        gr.addWidget(self.btn3, 2, 0)
        self.btn3.clicked.connect(self.setPath)

        btn4 = QtGui.QPushButton('Run create project', self)
        btn4.clicked.connect(self.createProject)
        gr.addWidget(btn4, 4, 4)

        closeBut = QtGui.QPushButton('Close', self)
        closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
        gr.addWidget(closeBut, 5, 4)

        self.lbl1 = QtGui.QLabel(MainWindow.projectName, self)
        gr.addWidget(self.lbl1, 0, 1)
        self.lbl2 = QtGui.QLabel(MainWindow.projectPath)
        gr.addWidget(self.lbl2, 1,1)
        self.lbl3 =QtGui.QLabel(MainWindow.projectFolder, self)
        gr.addWidget(self.lbl3, 3, 0, 3, 2)

        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Project Deployment')
        self.show()


    def showDialog(self):
        newtext, ok = QtGui.QInputDialog.getText(None, "Input", "Enter the name of the Project (in English)")
        if ok:
            self.lbl1.setText(str(newtext))
        MainWindow.projectName = str(newtext)
        return MainWindow.projectName

    def showSelector(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Select folder for the project", self.lbl2.text(), options)
        if foldername:
            self.lbl2.setText(parameters_test.update_filepath(foldername))
        MainWindow.projectPath = foldername + '/'
        return MainWindow.projectPath

    def setPath(self):
        MainWindow.projectFolder = MainWindow.projectPath + MainWindow.projectName
        tempdata = parameters_test.update_filepath(MainWindow.projectFolder)
        self.lbl3.setText(tempdata)
        MainWindow.projectFolder = tempdata
        return tempdata

    def createProject(self):
        print MainWindow.projectFolder
        inputdata = str(MainWindow.projectFolder)+'/'
        ProjectManagement.main_2(inputdata)



if __name__ == '__main__':
    # Создание окна
    # pyhtonProjectPath = 'C:/PAUL/Science/Coding_geography/'

    myApp = QtGui.QApplication(sys.argv)
    myProg = MainWindow()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())

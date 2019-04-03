# #!/usr/bin
# # -*-coding:utf-8-*-
# import os
# import sys
# import Create_Exec_MakeStructure
# from PyQt4 import QtGui, QtCore
# home = os.getenv("HOME")
#
#
#
# class MainWindow(QtGui.QWidget):
#     configFile = "No File"
#
# 
#
#     def __init__(self, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.build()
#
#     def build(self):
#
#
#         gr = QtGui.QGridLayout()
#
#
#         self.btn1 = QtGui.QPushButton('Select Configuration File', self)
#         gr.addWidget(self.btn1, 1, 0)
#         self.btn1.clicked.connect(self.showSelector)
#
#
#         btn3 = QtGui.QPushButton('Run create project', self)
#         btn3.clicked.connect(self.createProject)
#         gr.addWidget(btn3, 4, 4)
#
#         closeBut = QtGui.QPushButton('Close', self)
#         closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
#         gr.addWidget(closeBut, 5, 4)
#
#
#         self.lbl1 = QtGui.QLabel(MainWindow.configFile)
#         gr.addWidget(self.lbl1, 1, 1)
#
#         self.setLayout(gr)
#         self.setGeometry(300, 300, 250, 180)
#         self.setWindowTitle('Project Deployment')
#         self.show()
#
#
#
#
#     def showSelector(self):
#         conffilename = QtGui.QFileDialog.getOpenFileName(self, 'Select config file')
#         self.lbl1.setText(conffilename)
#         MainWindow.configFile = conffilename
#         print MainWindow.configFile
#         return MainWindow.configFile
#
#
#
#     def createProject(self):
#
#         print "The file is: ", MainWindow.configFile
#         inputdata = str(MainWindow.configFile)
#         print inputdata
#         Create_Exec_MakeStructure.main(inputdata)
#
#
#
# if __name__ == '__main__':
#     # Создание окна
#
#
#     myApp = QtGui.QApplication(sys.argv)
#     myProg = MainWindow()
#     myProg.show()
#     # Закрытие окна
#     sys.exit(myApp.exec_())

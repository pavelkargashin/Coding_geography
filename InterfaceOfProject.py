#!/usr/bin
# -*-coding:utf-8-*-
import os
import subprocess
import sys
import ProjectManagement
from PyQt4 import QtGui, QtCore
# Инициализация и параметры основного окна
class Window(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setGeometry(300, 100, 250, 150)
        self.setWindowTitle("Welcome to Wizard")

        self.button = QtGui.QPushButton('Create storage', self)
        self.button.clicked.connect(self.handButton)
        self.button.move(15,10)

    def handButton(self):
        print ('Hello World')
        ProjectManagement.main()


if __name__ == '__main__':
    # Создание окна
    # pyhtonProjectPath = 'C:/PAUL/Science/Coding_geography/'

    myApp = QtGui.QApplication(sys.argv)
    myProg = Window()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())

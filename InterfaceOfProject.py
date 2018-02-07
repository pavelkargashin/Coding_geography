#!/usr/bin
# -*-coding:utf-8-*-
import os
import subprocess
import sys
import ProjectManagement
from PyQt4 import QtGui, QtCore


class InputWindow(QtGui.QWidget):
    def __init__(self, parent = None):
        super(InputWindow,self).__init__(parent, QtCore.Qt.Window)
        self.build()


    def build(self):
        self.mainLayout = QtGui.QVBoxLayout()

        self.lbl = QtGui.QLabel("some text", self)
        self.edit = QtGui.QLineEdit(self)
        self.clbut = QtGui.QPushButton('close', self)
        self.clbut.clicked.connect(self.close_window)

        self.mainLayout.addWidget(self.lbl)
        self.mainLayout.addWidget(self.edit)
        self.mainLayout.addWidget(self.clbut)
        self.setLayout(self.mainLayout)


    def close_window(self):
        self.close()
        self.parent().nameLbl.setText(self.edit.text())


class MainWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.secondWin=None
        self.build()

    def build(self):
        self.setGeometry(300, 100, 250, 150)
        self.setWindowTitle("Welcome to Wizard")


        # Кнопки для работы
        self.nameButton = QtGui.QPushButton('Set Project name', self)
        self.nameButton.clicked.connect(self.inputWindow)
        self.nameLbl = QtGui.QLabel('temp', self)
        self.nameLbl.move(0, 100)

        self.show()

    def on_show(self):
        if not self.secondWin:
            self.secondWin = InputWindow(self)
        self.secondWin.edit.setText('that text')
        self.secondWin.show()

    def inputWindow(self):
        newtext, ok = QtGui.QInputDialog.getText(None, "Attention", "Password?")
        if ok:
            self.nameLbl.setText(newtext)







if __name__ == '__main__':
    # Создание окна
    # pyhtonProjectPath = 'C:/PAUL/Science/Coding_geography/'

    myApp = QtGui.QApplication(sys.argv)
    myProg = MainWindow()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())

#-*-coding:utf-8-*-
import os, sys
from PyQt4 import QtGui
from functools import partial
import xlwt
import re

field_list_sungai = [u'Year', u'RiverName', u'Location', u'KoordinatLS', u'KoordinatBT', u'Stage', u'Time',u'Temperatur', u'pH', u'DHL_MosCm', u'TDS_mgL', u'TSS_mgL', u'DO_mgL', u'BOD_mgL', u'COD_mgL', u'NO2_N_mgL', u'NO3_N_mgL', u'NH3_N_mgL', u'FreeChlori', u'TotalP_mgL', u'Phenol_mgL', u'OilAndFat_', u'Detergent_', u'FecalColif', u'TotalColif', u'Cyanide_mg', u'Sulfide_mg', u'Turbidity_', u'Cd_mgL', u'Fe_mgL', u'PO4_mgL', u'SO4_mgL', u'Pb_mgL', u'Mn_mgL', u'Zn_mgL', u'Cr_mgL']

class myProgramm(QtGui.QWidget):
    def __init__(self, parent=None):
        super(myProgramm, self).__init__()
        self.initUI()

    def initUI(self):

        # Создание сетки
        box = QtGui.QVBoxLayout(self)
        self.setLayout(box)

        scroll = QtGui.QScrollArea(self)
        box.addWidget(scroll)
        # scroll.setWidgetResizable(True)
        scrollContent = QtGui.QWidget(scroll)
        scrollLayout = QtGui.QVBoxLayout(scrollContent)
        scrollContent.setLayout(scrollLayout)
        for i in field_list_sungai:
            scrollLayout.addWidget(QtGui.QLabel(str(i)))
            scrollLayout.addWidget(QtGui.QLineEdit())
        scroll.setWidget(scrollContent)

        widgets = (scrollLayout.itemAt(i) for i in range(scrollLayout.count()))
        for widget in widgets:
            name = widget.objectName()
            print name


        self.setGeometry(50, 50, 1000, 500)
        self.setWindowTitle("My data input")
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    myApp = myProgramm()
    myApp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()





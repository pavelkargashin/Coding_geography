import sys
from PyQt4 import QtGui, QtCore
import Regionalization
field_list_sungai = [u'Temperatur', u'pH', u'DHL_MosCm', u'TDS_mgL', u'TSS_mgL', u'DO_mgL', u'BOD_mgL', u'COD_mgL', u'NO2_N_mgL', u'NO3_N_mgL', u'NH3_N_mgL', u'FreeChlori', u'TotalP_mgL', u'Phenol_mgL', u'OilAndFat_', u'Detergent_', u'FecalColif', u'TotalColif', u'Cyanide_mg', u'Sulfide_mg', u'Turbidity_', u'Cd_mgL', u'Fe_mgL', u'PO4_mgL', u'SO4_mgL', u'Pb_mgL', u'Mn_mgL', u'Zn_mgL', u'Cr_mgL']
field_list_sumur = [u'Temperatur', u'TDS_mgL', u'TSS_mgL', u'pH', u'BOD_mgL', u'COD_mgL', u'DO_mgL', u'TotalP_mgL', u'NO3_N_mgL', u'NH3_N_mgL', u'As_mgL', u'Co_mgL', u'Ba_mgL', u'B_mgL', u'Se_mgL', u'Cd_mgL', u'Cr_V_mgLI', u'Cu_mgL', u'Fe_mgL', u'Pb_mgL', u'Mn_mgL', u'Hg_mgL', u'Zn_mgL', u'Chloride_m', u'Cyanide_mg', u'Fluoride_m', u'NO2_N_mgL', u'Sulphate_m', u'FreeChlori', u'Sulfide_mg', u'Salinity_m', u'FecalColif', u'TotalColif', u'Gloss_A_mg', u'Gloss_B_mg', u'DHL_mgL', u'Phenol_mgL', u'OilAndFat_', u'Detergent_', u'PO4_mgL', u'Turbidity_']

class ProcessDataWindow(QtGui.QWidget):
    paramForMap = "Empty"
    env = "None"
    def __init__(self, parent=None):
        super(ProcessDataWindow, self).__init__()
        self.initUI()

    def initUI(self):

        introduction = QtGui.QLabel('Select data for analysis!', self)
        param1 = QtGui.QLabel('Year', self)
        self.param1List = QtGui.QComboBox()
        self.param1List.addItems(['2009', '2012', '2013', '2014', '2015', '2016', '2017'])
        param2 = QtGui.QLabel('Environment', self)

        self.b1 = QtGui.QRadioButton("Sungai")
        self.b1.setChecked(True)
        self.b1.toggled.connect(lambda:self.btnstate(self.b1))
        self.b2 = QtGui.QRadioButton("Sumur")
        self.b2.toggled.connect(lambda: self.btnstate(self.b2))

        # self.param2List = QtGui.QComboBox()
        # self.param2List.addItems(['Sungai', 'Sumur'])
        # self.param2List.currentIndexChanged.connect(self.selectionChange)


        param3 = QtGui.QLabel('Area Division', self)
        self.param3List = QtGui.QComboBox()
        self.param3List.addItems(['Administrative Units', 'Basins'])
        param4 = QtGui.QLabel('Statistics', self)
        self.param4List = QtGui.QComboBox()
        self.param4List.addItems(['Maximum', 'Mean', 'Minimum'])
        param5 = QtGui.QLabel('Chemistry', self)
        self.param5List = QtGui.QComboBox()
        self.param5List.addItems(field_list_sungai)


        self.CheckDataBut = QtGui.QPushButton('Check your selection!')
        self.CheckDataBut.clicked.connect(self.setData)
        self.CheckDataLabel = QtGui.QLabel('Your data is: ', self)

        self.PrintDataBut = QtGui.QPushButton('Print to console and RUN!')
        self.PrintDataBut.clicked.connect(self.toConsoleData)

        self.closeBut = QtGui.QPushButton('Close', self)
        self.closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)


        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(introduction, 1, 0)
        grid.addWidget(param1, 2, 0)
        grid.addWidget(self.param1List, 2, 1)
        grid.addWidget(param2, 3, 0)
        grid.addWidget(self.b1, 3, 1)
        grid.addWidget(self.b2, 3, 2)
        grid.addWidget(param3, 4, 0)
        grid.addWidget(self.param3List, 4, 1)
        grid.addWidget(param4, 5, 0)
        grid.addWidget(self.param4List, 5, 1)
        grid.addWidget(param5, 6, 0)
        grid.addWidget(self.param5List, 6, 1)

        grid.addWidget(self.CheckDataBut, 10, 0)
        grid.addWidget(self.CheckDataLabel, 10, 1)
        grid.addWidget(self.PrintDataBut, 11, 2)

        grid.addWidget(self.closeBut, 12, 2)

        self.setLayout(grid)
        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle("Data for analysis!")
        self.show()


    def setData(self):
        year = self.param1List.currentText()
        env = ProcessDataWindow.env
        regions = self.param3List.currentText()
        stat = self.param4List.currentText()
        chem = self.param5List.currentText()

        ProcessDataWindow.paramForMap = regions+' -- '+env+' -- '+stat+' -- '+year+' -- '+chem
        self.CheckDataLabel.setText(ProcessDataWindow.paramForMap)
        return ProcessDataWindow.paramForMap


    def toConsoleData(self):
        year = self.param1List.currentText()
        env = ProcessDataWindow.env
        regions = self.param3List.currentText()
        stat = self.param4List.currentText()
        chem = self.param5List.currentText()
        Regionalization.regionalisation_process(regions, env, stat, year, chem)

    def selectionChange(self):
        self.param5List.addItems()

    def btnstate(self, b):

        if b.text() == "Sungai":
            self.param5List.clear()
            self.param5List.addItems(field_list_sungai)

        if b.text() == "Sumur":
            self.param5List.clear()
            self.param5List.addItems(field_list_sumur)
        ProcessDataWindow.env = b.text()
        return ProcessDataWindow.env




def main():
    app = QtGui.QApplication(sys.argv)
    myApp = ProcessDataWindow()
    myApp.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


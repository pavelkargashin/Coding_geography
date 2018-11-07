#!/usr/bin
# -*-coding:utf-8-*-
import os
import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL
import configparser

home = os.getenv("HOME")

# defs to create congigfile
def create_config(ProjectFolder, ConfigFileName):
    config = configparser.ConfigParser()
    config.add_section('Paths')
    config.set('Paths', 'ProjectFolder', ProjectFolder)
    config.set('Paths', 'InputData', ProjectFolder + "InputData/")
    config.set('Paths', 'TempData', ProjectFolder + "TempData/")
    config.set('Paths', 'OutputData', ProjectFolder + "OutputData/")
    config.set('Paths', 'GISDataName', "GISEcologyBali")
    config.set('Paths', 'Decoration', ProjectFolder + "Decoration/")
    config.set('Paths', 'ThematicDatasetName', 'ThematicData')
    config.set('Paths', 'BasemapDatasetName', 'BasemapData')
    config.set('Paths', 'AnalysisDatasetName', 'AnalysisData')
    config.set('Paths', 'mxdName', ProjectFolder+'GISEcologyBali.mxd')

    config.add_section('ImportParameters')
    config.set('ImportParameters', 'fieldname', 'Year')
    config.set('ImportParameters', 'fieldname_2', 'Stage')

    config.add_section('ProcessingConstants')
    config.set('ProcessingConstants', 'Danau', 'AirDanau')
    config.set('ProcessingConstants', 'Sumur', 'AirSumur')
    config.set('ProcessingConstants', 'Sungai', 'AirSungai')
    config.set('ProcessingConstants', 'Laut', 'AirLaut')

    config.add_section('Dictionaries')
    config.set('Dictionaries', 'field_dict', "{Danau: 'LakeName', Sungai: 'RiverName',Sumur: 'Area',Laut: 'Point'}")
    config.set('Dictionaries', 'polyg_attr_name_dict', "{Danau: 'Name', Sungai: 'Basin',Sumur: 'Regency'}")
    config.set('Dictionaries', 'centroid_dict', "{Danau: TempData+'/Lake_Center.shp',Sungai: TempData+'/Basin_Center.shp', Sumur: TempData+'/Regency_Center.shp'}")
    config.set('Dictionaries', 'polyg_name_dict', "{Danau: ProjectFolder + GISDataName + '.gdb/' + BasemapDatasetName + '/Lakes',Sungai: ProjectFolder + GISDataName + '.gdb/' + BasemapDatasetName + '/Basins', Sumur: ProjectFolder + GISDataName + '.gdb/' + BasemapDatasetName + '/Regency'}")
    config.set('Dictionaries', 'end_field', "{Danau: 'PO4_mgL', Sungai: 'Cr_mgL', Sumur: 'Turbidity_', Laut: 'TotalColif'}")
    config.set('Dictionaries', 'first_field', "{Danau: 'DHL_mgL', Sungai: 'TDS_mgL', Sumur: 'TDS_mgL', Laut: 'Color_CU'}")

    config.add_section('FieldLists')
    config.set('FieldLists', 'field_list_sungai', "[u'TDS_mgL', u'TSS_mgL', u'DO_mgL', u'BOD_mgL', u'COD_mgL', u'NO2_N_mgL', u'NO3_N_mgL', u'NH3_N_mgL', u'FreeChlori', u'TotalP_mgL', u'Phenol_mgL', u'OilAndFat_', u'Detergent_', u'FecalColif', u'TotalColif', u'Cyanide_mg', u'Sulfide_mg', u'Turbidity_', u'Cd_mgL', u'Fe_mgL', u'PO4_mgL', u'SO4_mgL', u'Pb_mgL', u'Mn_mgL', u'Zn_mgL', u'Cr_mgL']")
    config.set('FieldLists', 'field_list_sumur', "[u'Temperatur', u'TDS_mgL', u'TSS_mgL', u'pH', u'BOD_mgL', u'COD_mgL', u'DO_mgL', u'TotalP_mgL',u'NO3_N_mgL', u'NH3_N_mgL', u'As_mgL', u'Co_mgL', u'Ba_mgL', u'B_mgL', u'Se_mgL', u'Cd_mgL',u'Cr_V_mgLI', u'Cu_mgL', u'Fe_mgL', u'Pb_mgL', u'Mn_mgL', u'Hg_mgL', u'Zn_mgL', u'Chloride_m',u'Cyanide_mg', u'Fluoride_m', u'NO2_N_mgL', u'Sulphate_m', u'FreeChlori', u'Sulfide_mg',u'Salinity_m', u'FecalColif', u'TotalColif', u'Gloss_A_mg', u'Gloss_B_mg', u'DHL_mgL',u'Phenol_mgL', u'OilAndFat_', u'Detergent_', u'PO4_mgL', u'Turbidity_']")

    with open(ProjectFolder+ConfigFileName, 'w') as config_file:
        config.write(config_file)


def update_filepath(inputpath):
    temppath = str(inputpath)
    outputpath = temppath.replace('\\', '/')
    return outputpath


#Description of the window
class MainWindow(QtGui.QWidget):
    projectPath = "NoFolder"
    ConfigFileName = "CONFIGURATION"
    projectPath.replace('\\', '/')
    projectFolder = 'None'


    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.build()

    def build(self):

        gr = QtGui.QGridLayout()

        self.btn1 = QtGui.QPushButton()
        self.btn1.setText('Set Name')
        gr.addWidget(self.btn1, 1, 0)
        self.btn1.clicked.connect(self.showDialog)

        self.btn2 = QtGui.QPushButton('Select path', self)
        gr.addWidget(self.btn2, 0, 0)
        self.btn2.clicked.connect(self.showSelector)

        self.btn3 = QtGui.QPushButton('Set Path', self)
        gr.addWidget(self.btn3, 2, 0)
        self.btn3.clicked.connect(self.setPath)

        self.btn4 = QtGui.QPushButton()
        self.btn4.setText('Create Configuration')
        gr.addWidget(self.btn4, 3, 0)
        self.connect(self.btn4, SIGNAL("clicked()"), self.createConf)



        closeBut = QtGui.QPushButton('Close', self)
        closeBut.clicked.connect(QtCore.QCoreApplication.instance().quit)
        gr.addWidget(closeBut, 5, 4)

        self.lbl1 = QtGui.QLabel(MainWindow.ConfigFileName, self)
        gr.addWidget(self.lbl1, 1, 1)
        self.lbl2 = QtGui.QLabel(MainWindow.projectPath)
        gr.addWidget(self.lbl2, 0, 1)
        self.lbl3 = QtGui.QLabel(MainWindow.projectPath, self)
        gr.addWidget(self.lbl3, 3, 0, 3, 2)

        self.setLayout(gr)
        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('Create Configuration File')
        self.show()


    def showDialog(self):
        newtext, ok = QtGui.QInputDialog.getText(None, "Input", "Enter the name of the Project (in English)")
        if ok:
            self.lbl1.setText(str(newtext))
        MainWindow.ConfigFileName = str(newtext)
        return MainWindow.ConfigFileName

    def showSelector(self):
        options = QtGui.QFileDialog.DontResolveSymlinks | QtGui.QFileDialog.ShowDirsOnly
        foldername = QtGui.QFileDialog.getExistingDirectory(self, "Select folder for the project", self.lbl2.text(),
                                                            options)
        if foldername:
            self.lbl2.setText(update_filepath(foldername))
        MainWindow.projectPath = foldername + '/'
        return MainWindow.projectPath

    def setPath(self):
        MainWindow.projectFolder = MainWindow.projectPath + MainWindow.ConfigFileName+'.ini'
        tempdata = update_filepath(MainWindow.projectFolder)
        self.lbl3.setText(tempdata)
        MainWindow.projectFolder = tempdata
        return tempdata

    def createConf(self):
        temp = MainWindow.projectPath.replace('\\', '/')
        create_config(temp, MainWindow.ConfigFileName)
        print ('WOW!')
        return

if __name__ == '__main__':
    # Создание окна
    # pyhtonProjectPath = 'C:/PAUL/Science/Coding_geography/'

    myApp = QtGui.QApplication(sys.argv)
    myProg = MainWindow()
    myProg.show()
    # Закрытие окна
    sys.exit(myApp.exec_())

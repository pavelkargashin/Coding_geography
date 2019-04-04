# -*-coding:utf-8-*-
import sys
import csv
#import General_Tools_ConfigFile as GTC
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog, QVBoxLayout, QLabel, QWidget, QApplication,\
    QPushButton, QLineEdit, QFormLayout, QScrollArea


#filePath = filePath = GTC.get_setting('CONFIGURATION', 'Paths', 'inputdata')
fileName = "Laut_add.csv"
field_list_sungai = [u'Point', u'Location', u'Longitude',
                     u'Latitude', u'Year', u'Stage',
                     u'Color_CU', u'Smell', u'Brightness',
                     u'Turbidity_', u'TSS_mgL', u'Waste',
                     u'OilCoating', u'Temperatur', u'pH',
                     u'Salinity_m', u'DO_mgL', u'BOD5_mgL',
                     u'COD_mgL', u'TotalAmmon', u'NO2_N_mgL',
                     u'NO3_N_mgL', u'PO4_P_mgL', u'Cyanide_mg',
                     u'Sulfide_mg',  u'FreeChlori', u'CrudeOil_m',
                     u'Phenol_mgL', u'Pesticide_', u'PCB_mgL',
                     u'Phospat_mg', u'Cd_mgL', u'TotalColif']

str_list = [0, 1, 5]


def is_number(val):
    try:
        float(val)
        if float(val) > 0:
            return True
    except ValueError:
        return False


def create_csv(filename, fieldlist):
    with open(filename, 'wb') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(fieldlist)


def write_to_csv(indata, destfile):
    with open(destfile, 'ab') as resultFile:
        wr = csv.writer(resultFile, dialect='excel')
        wr.writerow(indata)


class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.resetBut = QPushButton()
        self.resetBut.setText("Reset")

        self.checkBut = QPushButton()
        self.checkBut.setText("Verify data")

        self.writeBut = QPushButton()
        self.writeBut.setText("Write data to Excel")

        self.clsBut = QPushButton()
        self.clsBut.setText("Close dialog")

        # Создание сетки
        layout = QFormLayout()

        scroll = QScrollArea(self)
        layout.addWidget(scroll)
        # scroll.setWidgetResizable(True)
        scrollcontent = QWidget(scroll)
        scrlayout = QVBoxLayout(scrollcontent)
        scrollcontent.setLayout(scrlayout)
        for i in field_list_sungai:
            scrlayout.addWidget(QLabel(str(i)))
            scrlayout.addWidget(QLineEdit(str('Enter data')))
        scroll.setWidget(scrollcontent)

        layout.addWidget(self.checkBut)
        layout.addWidget(self.writeBut)
        layout.addWidget(self.resetBut)
        layout.addWidget(self.clsBut)

        self.setLayout(layout)
        self.connect(self.checkBut, SIGNAL("clicked()"), self.check_click)
        self.connect(self.resetBut, SIGNAL("clicked()"), self.reset_click)
        self.connect(self.writeBut, SIGNAL("clicked()"), self.write_click)
        self.connect(self.clsBut, SIGNAL("clicked()"), self.cls_click)
        self.setWindowTitle("Laut new data")

    def write_click(self):
        print ("write data to Excel file!")
        line_edits = self.findChildren(QLineEdit)
        list2write = list()
        for item in range(len(line_edits)):
            list2write.append(str(line_edits[item].text()))
        write_to_csv(list2write, fileName)
        print('Your data has been appended!')

    def check_click(self):
        print('Data will be verified')
        line_edits = self.findChildren(QLineEdit)
        current_data = list()
        for item in range(len(line_edits)):
            val = str(line_edits[item].text()).replace(',', '.')
            line_edits[item].setText(val)
            current_data.append(str(val))
        if is_number(current_data[4]) == False:
            line_edits[4].setText('Bad Value!')
        if is_number(current_data[3]) == False:
            line_edits[3].setText('Bad Value!')
        if is_number(current_data[2]) == False:
            line_edits[2].setText('Bad Value!')
        for item in range(6, len(current_data)):
            if is_number(current_data[item]) == False:
                line_edits[item].setText('Bad Value!')
            else:
                continue
        for val in str_list:
            if is_number(current_data[val]) == True:
                 line_edits[val].setText('Bad Value!')
            else:
                continue
        print ('Current data is {}'.format(current_data))

    def reset_click(self):
        print('your data has been erased!')
        line_edits = self.findChildren(QLineEdit)
        for item in range(len(line_edits)):
            line_edits[item].setText('Enter Data')  # постоянная часть кода для обнуления данных



    def cls_click(self):
        self.close()


app = QApplication(sys.argv)
myApp = Form()
myApp.show()
create_csv(fileName, field_list_sungai)
app.exec_()

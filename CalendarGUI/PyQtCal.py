import sys
from datetime import datetime, timedelta

import pandas as pd
import pyodbc
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDate, QRect, QSize, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QCalendarWidget, QDialog,
                             QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                             QMainWindow, QMenuBar, QPushButton, QVBoxLayout,
                             QWidget)


class Window(QDialog):
        def __init__(self):
                super().__init__()
                win = QWidget()
                self.title = "Calendar Application"
                self.top = 100
                self.left = 100
                self.width = 400
                self.height = 400
                self.InitWindow()

        def InitWindow(self):
                #self.setWindowIcon(QtGui.QIcon("heading.png"))
                self.setWindowTitle(self.title)
                self.setGeometry(self.top, self.left, self.width, self.height)
                self.createMenu()
                self.createHeader()
                self.createHomeLayout()
                self.show()


        def createHeader(self):
                gboxLayout = QGridLayout()
                self.label = QLabel("Calendar Application")
                gboxLayout.addWidget(self.label, 1, 1)
                self.header_groupBox = QGroupBox()
                self.header_groupBox.setLayout(gboxLayout)

        def createMenu(self):
                mainMenu = QMenuBar()
                fileMenu = mainMenu.addMenu("File")
                helpMenu = mainMenu.addMenu("Help")

                exitAction = QAction('Exit', self)
                helpAction = QAction('About Us', self)

                fileMenu.addAction(exitAction)
                helpMenu.addAction(helpAction)

        def createHomeLayout(self):
### --------------------------- ACTIVITY Widget --------------------------------- ###

                hbox = QHBoxLayout()
                self.activity_groupBox = QGroupBox("Activities")
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.activity_groupBox.setFont(font) 
                self.gridLayout = QGridLayout()

                self.button1 = QPushButton("Activity-1", self)
                self.button1.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button1.setFont(font)
                self.gridLayout.addWidget(self.button1, 0, 0)

                self.button2 = QPushButton("Activity-2", self)
                self.button2.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button2.setFont(font)
                self.gridLayout.addWidget(self.button2, 0, 1)

                self.button3 = QPushButton("Activity-3", self)
                self.button3.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button3.setFont(font)
                self.gridLayout.addWidget(self.button3, 0, 2)

                self.button4 = QPushButton("Activity-4", self)
                self.button4.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button4.setFont(font)
                self.gridLayout.addWidget(self.button4, 1, 0)

                self.button5 = QPushButton("Activity-5", self)
                self.button5.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button5.setFont(font)
                self.gridLayout.addWidget(self.button5, 1, 1)

                self.button6 = QPushButton("Activity-6", self)
                self.button6.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button6.setFont(font)
                self.gridLayout.addWidget(self.button6, 1, 2)

                self.button7 = QPushButton("Activity-7", self)
                self.button7.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button7.setFont(font)
                self.gridLayout.addWidget(self.button7, 2, 0)

                self.button8 = QPushButton("Activity-8", self)
                self.button8.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button8.setFont(font)
                self.gridLayout.addWidget(self.button8, 2, 1)

                self.button9 = QPushButton("Activity-9", self)
                self.button9.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button9.setFont(font)
                self.gridLayout.addWidget(self.button9, 2, 2)

                self.button10 = QPushButton("Activity-10", self)
                self.button10.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button10.setFont(font)
                self.gridLayout.addWidget(self.button10, 3, 0)

                self.button11 = QPushButton("Activity-11", self)
                self.button11.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button11.setFont(font)
                self.gridLayout.addWidget(self.button11, 3, 1)

                self.button12 = QPushButton("Activity-12", self)
                self.button12.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button12.setFont(font)
                self.gridLayout.addWidget(self.button12, 3, 2)

                self.button13 = QPushButton("Activity-13", self)
                self.button13.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button13.setFont(font)
                self.gridLayout.addWidget(self.button13, 4, 0)

                self.button14 = QPushButton("Activity-14", self)
                self.button14.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button14.setFont(font)
                self.gridLayout.addWidget(self.button14, 4, 1)

                self.button15 = QPushButton("Activity-15", self)
                self.button15.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button15.setFont(font)
                self.gridLayout.addWidget(self.button15, 4, 2)

                self.button16 = QPushButton("Activity-16", self)
                self.button16.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button16.setFont(font)
                self.gridLayout.addWidget(self.button16, 5, 0)

                self.button17 = QPushButton("Activity-17", self)
                self.button17.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button17.setFont(font)
                self.gridLayout.addWidget(self.button17, 5, 1)

                self.button18 = QPushButton("Activity-18", self)
                self.button18.setMinimumHeight(40)
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.button18.setFont(font)
                self.gridLayout.addWidget(self.button18, 5, 2)

                self.activity_groupBox.setLayout(self.gridLayout)
                #self.report_groupBox.setLayout(gridLayout)

### ------------------------ REPORTS Widget -------------------------------- ###

                self.report_groupBox = QGroupBox("Reports")
                font = QtGui.QFont()
                font.setFamily("Verdana")
                font.setBold(True)
                self.report_groupBox.setFont(font)

                vbox = QVBoxLayout(self)

                cal = QCalendarWidget(self)
                cal.setGridVisible(True)
                cal.clicked[QDate].connect(self.showDate)
                vbox.addWidget(cal)

                self.lbl = QLabel(self)
                date = cal.selectedDate()
                self.lbl.setText(date.toString("yyyy-MM-dd"))
                vbox.addWidget(self.lbl)

                hbox.addWidget(self.activity_groupBox)
                hbox.addWidget(self.report_groupBox)
                self.setLayout(hbox)

        def close(self):
                self.close()

        #def recruitWindow(self):
        def showDate(self, date):
                self.lbl.setText(date.toString("yyyy-MM-dd"))

class Scheduler(QCalendarWidget):
        def __init__(self, parent=None):
                super().__init__(parent)
                self.events = {
                        QDate(2019, 5, 24): ["Bob's birthday"],
                        QDate(2019, 5, 19): ["Alice's birthday"]
                        }

        def paintCell(self, painter, rect, date):
                super().paintCell(painter, rect, date)
                if date in self.events:
                        painter.setBrush(Qt.red)
                        painter.drawEllipse(rect.topLeft() + QPoint(12, 7), 3, 3)

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())

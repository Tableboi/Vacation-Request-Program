import datetime

import pyodbc
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import (QColor, QFont, QTextCharFormat, QTextLength,
                         QTextTableFormat)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateTimeEdit,
                             QHBoxLayout, QLabel, QMainWindow, QSpinBox,
                             QTextBrowser, QVBoxLayout, QWidget)


class Ui_CalendarWidget(object):
    def setupUi(self, CalendarWidget):
        CalendarWidget.setObjectName("CalendarWidget")
        CalendarWidget.resize(1200, 900)
        CalendarWidget.setMinimumSize(QtCore.QSize(0, 0))
        CalendarWidget.setMaximumSize(QtCore.QSize(1200, 900))
        CalendarWidget.setStyleSheet("background-color: rgb(200, 200, 200);")
        self.centralWidget = QtWidgets.QWidget(CalendarWidget)
        self.centralWidget.setObjectName("centralWidget")
        self.Header = QtWidgets.QTextEdit(self.centralWidget)
        self.Header.setEnabled(False)
        self.Header.setGeometry(QtCore.QRect(-10, 0, 1300, 110))
        self.Header.setMinimumSize(QtCore.QSize(1300, 110))
        self.Header.setMaximumSize(QtCore.QSize(1300, 110))
        self.Header.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(255, 255, 255);\n"
"border-width : 1.2px;\n"
"border-style:inset;")
        self.Header.setObjectName("Header")
        self.LECTURP = QtWidgets.QLabel(self.centralWidget)
        self.LECTURP.setGeometry(QtCore.QRect(512, 2, 180, 61))
        self.LECTURP.setStyleSheet("color: rgb(0, 176, 240);\n"
"font: 8pt \"MS Shell Dlg 2\";\n"
"text-decoration: underline;\n"
"background-color: rgb(255, 255, 255);\n"
"font: 28pt \"Calbri\";\n"
"text-decoration: underline;")
        self.LECTURP.setObjectName("LECTURP")
        self.LecturpBanner = QtWidgets.QLabel(self.centralWidget)
        self.LecturpBanner.setGeometry(QtCore.QRect(320, 60, 561, 31))
        self.LecturpBanner.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 176, 240);\n"
"font: 14pt \"Calibri\";")
        self.LecturpBanner.setObjectName("LecturpBanner")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralWidget)
        self.calendarWidget.setGeometry(QtCore.QRect(30, 110, 1141, 661))
        self.calendarWidget.setStyleSheet("alternate-background-color: rgb(255, 255, 255);\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"background-color: rgb(200, 200, 200);\n"
"selection-background-color: rgb(255, 0, 0);")
        self.calendarWidget.setObjectName("calendarWidget")
        self.DateInfoOutput = QtWidgets.QLabel(self.centralWidget)
        self.DateInfoOutput.setGeometry(QtCore.QRect(30, 778, 1141, 97))
        self.DateInfoOutput.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-color: rgb(0, 0, 0);\n"
"font: 16pt \"Calibri\";\n"
"border-width : 1.2px;\n"
"border-style:inset;")
        self.DateInfoOutput.setText("")
        self.DateInfoOutput.setObjectName("DateInfoOutput")
        self.WeekNumber = QtWidgets.QLabel(self.centralWidget)
        self.WeekNumber.setGeometry(QtCore.QRect(56, 168, 113, 49))
        self.WeekNumber.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 16pt \"MS Shell Dlg 2\";")
        self.WeekNumber.setObjectName("WeekNumber")
        self.calendarWidget.raise_()
        self.Header.raise_()
        self.LECTURP.raise_()
        self.LecturpBanner.raise_()
        self.DateInfoOutput.raise_()
        self.WeekNumber.raise_()
        CalendarWidget.setCentralWidget(self.centralWidget)
        self.statusbar = QtWidgets.QStatusBar(CalendarWidget)
        self.statusbar.setObjectName("statusbar")
        CalendarWidget.setStatusBar(self.statusbar)

        self.retranslateUi(CalendarWidget)
        QtCore.QMetaObject.connectSlotsByName(CalendarWidget)

        self.editor = QTextBrowser()


        self.calendarWidget.clicked[QDate].connect(self.dateClicked)

        cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=SOPCP01DE;"
            "Database=PulseCoreTest5;"
            "UID=PCDev2;"
            "PWD=PCCSDev2PC5_!;")

        cnxn = pyodbc.connect(cnxn_str)
        cursor = cnxn.cursor()
        
        Current_Day = datetime.date.today().strftime("%A,")
        Current_Date = datetime.date.today().strftime("%d")
        Current_Month = datetime.date.today().strftime("%B")

        Combined_Date = ("It is a " + Current_Day + " It is the " + Current_Date + " of " + Current_Month)

        Combined_Date = str(Combined_Date)

        self.DateInfoOutput.setText(Combined_Date)


        #This is where the SQL Data is converted to d/M/yyyy and is then highlighted onto the calendar widget itself.

        cnxn = pyodbc.connect(cnxn_str)
        cursor = cnxn.cursor()
        cursor.execute (" SELECT [dDateStart], [dDateEnd] FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]")

        date_format = "d/M/yyyy"
        cell_format = QtGui.QTextCharFormat()
        cell_format.setBackground(QtGui.QColor("lightblue"))

    def dateClicked(self, clickedDate):
        cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=SOPCP01DE;"
            "Database=PulseCoreTest5;"
            "UID=PCDev2;"
            "PWD=PCCSDev2PC5_!;")
        cnxn = pyodbc.connect(cnxn_str) 
        # This is the code for the database cursor 
        cursor = cnxn.cursor()
        Count = 1
        cursor.execute(' SELECT [dDateStart], [dDateEnd] FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]', (Count,))
        RawDay = cursor.fetchone()
        Day = str(RawDay)
        Day = Day.replace('(', '')
        Day = Day.replace(')', '')
        Day = Day.replace(',', '')
        Day = int(Day)

        cursor.execute(' SELECT [dDateStart], [dDateEnd] FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]', (Count,))
        RawMonth = cursor.fetchone()
        Month = str(RawMonth)
        Month = Month.replace('(', '')
        Month = Month.replace(')', '')
        Month = Month.replace(',', '')
        Month = int(Month)

        cursor.execute(' SELECT [dDateStart], [dDateEnd] FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]', (Count,))
        RawYear = cursor.fetchone()
        Year = str(RawDay)
        Year = Year.replace('(', '')
        Year = Year.replace(')', '')
        Year = Year.replace(',', '')
        Year = int(Year)        


        Current_Day = datetime.date.today().strftime("%A,")
        Current_Date = datetime.date.today().strftime("%d")
        Current_Month = datetime.date.today().strftime("%B")


        Combined_Date = ("It is a " + Current_Day + " It is the " + Current_Date + " of " + Current_Month)

        Combined_Date = str(Combined_Date)

        self.DateInfoOutput.setText(Combined_Date)

        cursor = self.editor.textCursor()

        All_Dates = (Day, Month, Year)

        self.selectedDate = QDate.currentDate()
        cnxn = pyodbc.connect(cnxn_str) 
        cursor = cnxn.cursor() 
        cursor.execute(
            ' SELECT [dDateStart], [dDateEnd] FROM [PulseCoreTest5].[dbo].[PC_VacationsRequests]', 
            (clickedDate.day(), clickedDate.month(), clickedDate.year()))
        result = cursor.fetchone()

        self.Date = (clickedDate.day() , '/' , clickedDate.month() , '/' , clickedDate.year())



        if result:
            self.DateInfoOutput.setText(result[0])


        else:
            self.DateInfoOutput.setText(Combined_Date)








    def retranslateUi(self, CalendarWidget):
        _translate = QtCore.QCoreApplication.translate
        CalendarWidget.setWindowTitle(_translate("CalendarWidget", "CalendarWidget"))
        self.LECTURP.setText(_translate("CalendarWidget", "LECTURP"))
        self.LecturpBanner.setText(_translate("CalendarWidget", "Lecture, Exam, Coursework, Timetable, Uploader and Reminder Program."))
        self.WeekNumber.setText(_translate("CalendarWidget", "Week No."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CalendarWidget = QtWidgets.QMainWindow()
    ui = Ui_CalendarWidget()
    ui.setupUi(CalendarWidget)
    CalendarWidget.show()
    sys.exit(app.exec_())

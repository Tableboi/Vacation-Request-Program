import sys, os
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from PyQt5.QtCore import QDate, Qt, QRect
from PyQt5.QtGui import (
    QFont,
    QColor,
    QBrush,
    QPainter,
    QTextCharFormat,

)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QTextEdit,
    QApplication,
    QTableWidget,
    QCalendarWidget,
    QTableWidgetItem,
)

client = MongoClient("localhost", 27017)
db     = client["mydb"]
coll   = db["appointments"]

class Calendar(QCalendarWidget):    
    
    def __init__(self, parent=None):
        super(Calendar, self).__init__(parent)

class Appointments():

    def appointments(self):
        appts = []
        now   = datetime.now()
        today = now.strftime('%m-%d-%Y')
        
        data = coll.find({}, {'_id': 0, 'date': 1, 'time': 1, 'place': 1, 'note': 1}).sort('date')        
        
        for _d in data:
            if _d['date'] < today:
                pass
            else:
                date, time, place, note = _d['date'][:5], _d['time'], _d['place'], _d['note']                
                
                appts.append([date, time, place, note])
        return appts
        
class MyApp(QWidget): 

    def __init__(self):
        super(MyApp, self).__init__()
        self.initUI()

    def initUI(self):
        self.left   = 1138
        self.top    = 30
        self.width  = 302
        self.height = 370
        self.appointments = Appointments()
        self.cal = QCalendarWidget( self )
        format = QTextCharFormat()        
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)        

        qdim = "QPushButton {color: rgba(54, 136, 200, 250); background-color: black; }"
        canda_10 = QFont("Candalara", 10)
        canda_11 = QFont( "Candalara", 11 )
        segoe_9  = QFont('Segoe UI', 9)        
        
        format   = self.cal.weekdayTextFormat( Qt.Saturday)
        format.setForeground(QBrush( Qt.darkCyan, Qt.SolidPattern))        
        
        self.cal.setWeekdayTextFormat( Qt.Saturday, format )
        self.cal.setWeekdayTextFormat( Qt.Sunday, format )        
        
        self.cal.setVerticalHeaderFormat(self.cal.NoVerticalHeader)
        self.cal.setGridVisible(False)
        self.cal.setGeometry(0, 0, 292, 221)
        self.cal.setFont(segoe_9)
        self.cal.setStyleSheet(
            "QCalendarWidget QAbstractItemView{background-color: black; color: rgba(162,201,229,255); selection-background-color: rgb(20,20,20); selection-color: rgb(200,150,255); selection-border: 1px solid black;}"
            
            "QCalendarWidget QWidget{alternate-background-color: rgb(20, 20, 20); color: gray;}"

            "QCalendarWidget QToolButton{background-color: black; color: rgb(125,125,125); font-size: 14px; font: bold; width: 70px; border: none;}"
            
            "QCalendarWidget QToolButton#qt_calendar_prevmonth{qproperty-icon: url(left_arrow.png);}"          
            
            "QCalendarWidget QToolButton#qt_calendar_nextmonth{qproperty-icon: url(right_arrow.png);}"
            )
    def QPushButton(self):    
        self.button = QPushButton(self)
        self.button.setStyleSheet(qdim)
        self.button.setFont(canda_11)
        self.button.setText("EXIT")
        self.button.setGeometry(10, 240, 281, 90)
        self.button.clicked.connect(self.exit)        
 
        self.cal.clicked[QDate].connect(self.showDate)        
        
        self.appt_table = QTableWidget( self )
        self.appt_table.setGeometry( QRect( 10, 240, 281, 90 ) )
        self.appt_table.setStyleSheet(
                "QTableWidget {color: rgb(135,135,135); background-color: black; border: none;}"
        ) 
        self.appt_table.horizontalHeader().hide()
        self.appt_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.appt_table.setFont( canda_10 )
        self.appt_table.verticalHeader().setVisible( False )     
        
        data = self.appointments.appointments()
        df = pd.DataFrame(data)
        self.display_data(df)
        self.show()

    def display_data(self, var):
        self.appt_table.setColumnCount( len( var.columns ) )
        self.appt_table.setRowCount( len( var.index ) )

        for i in range( len( var.index ) ):
            for j in range( len( var.columns ) ):
                self.appt_table.setItem( i, j, QTableWidgetItem( str( var.iat[i, j] ) ) )
        self.appt_table.resizeColumnsToContents()

    def showDate(self, date):
        now =  QDate.currentDate()
        select_date = self.cal.selectedDate()
        if select_date < now:
            pass
        else:
            string_date = str(select_date.toPyDate())
            self.event_form(string_date)

    def event_form(self, string_date):
        with open('string_date.txt', 'w') as file:
            file.write(string_date)
        os.system( r"start /min python event_form.py" )

    def paintEvent(self, e):
        self.painter = QPainter( self )
        self.painter.begin( self )
        self.painter.setPen(QColor(75, 75, 75))
        self.painter.drawLine(50, 230, 250, 230)
        self.painter.drawLine(50, 340, 250, 340)
        self.painter.end()

    def exit(self):
        self.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        	print('Closing Window...')

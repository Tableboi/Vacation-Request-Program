import sys
from datetime import datetime
from pymongo import MongoClient
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import (
    QPen,
    QFont,
    QColor,
    QBrush,
    QPainter,
)
from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QComboBox,
    QApplication,
)


client = MongoClient("localhost", 27017)
db     = client["mydb"]
coll   = db["appointments"]



class EventForm(QWidget):
    def __init__(self):
        super(EventForm, self).__init__()
        self.initUI()

    def initUI(self):
        self.left   = 1139
        self.top    = 253
        self.width  = 301
        self.height = 370

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)        
        
        qdim = "QPushButton {color: rgba(54, 136, 200, 250); background-color: black; }" 
        
        segoe_9  = QFont( 'Segoe UI', 9 )
        segoe_16 = QFont( "Segoe UI", 16 )
        canda_10 = QFont( "Candalara", 10 )
        canda_11 = QFont( "Candalara", 11 )
        canda_12 = QFont( "Candalara", 12 )

        times = [
            'All Day','5:00 AM', '5:30 AM', '6:00 AM', '6:30 AM',
            '7:00 AM', '7:30 AM', '8:00 AM', '8:30 AM', '9:00 AM',
            '9:30 AM', '10:00 AM', '10:30 AM', '11:00 AM',
            '11:30 AM', 'Noon', '12:30 PM', '1:00 PM', '1:30 PM',
            '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM',
            '4:30 PM', '5:00 PM', '5:30 PM', '6:00 PM',
        ]

        with open('string_date.txt', "r") as file:
            data = file.read()
        day  = str(num.strftime( '%A' ))
        date = str(num.strftime('%m-%d-%Y'))        
        
        self.date_data = QLabel(self)
        self.date_data.setGeometry( 0, 15, 301, 40 )
        self.date_data.setStyleSheet( "QLabel {color: rgba(125,125,125,255); background-color: black;}" )
        self.date_data.setFont( segoe_16 )
        self.date_data.setAlignment(Qt.AlignCenter)
        self.date_data.setText(day + "  " + date)

        self.time_label = QLabel(self)
        self.time_label.setGeometry(15, 70, 80, 40)
        self.time_label.setStyleSheet( "QLabel {color: rgba(125,125,125,255); background-color: black;}" )
        self.time_label.setFont(canda_11)
        self.time_label.setText("Time")

        self.place_label = QLabel(self)
        self.place_label.setGeometry(15, 115, 80, 40)
        self.place_label.setStyleSheet( "QLabel {color: rgba(125,125,125,255); background-color: black;}" )
        self.place_label.setFont(canda_11)
        self.place_label.setText("Place")

        self.note_label = QLabel(self)
        self.note_label.setGeometry( 15, 160, 80, 40 )
        self.note_label.setStyleSheet( "QLabel {color: rgba(125,125,125,255); background-color: black;}" )
        self.note_label.setFont( canda_11 )
        self.note_label.setText( "Note" )        
        
        self.time_cbox = QComboBox( self )
        self.time_cbox.setGeometry( 70, 75, 100, 30 )
        self.time_cbox.setStyleSheet( "QComboBox {color: rgba(125,125,125,255); background-color: black;}" )
        self.time_cbox.setFont( canda_11 )
        for time in times:
            self.time_cbox.addItem(time)
        self.time_cbox.currentIndexChanged.connect(self.selectionchange)        

        self.place_edit = QLineEdit( self )
        self.place_edit.setGeometry(70, 120, 215, 30 )
        self.place_edit.setStyleSheet( "QLineEdit {color: rgba(125,125,125,255); background-color: rgba(29, 29, 29, 150); border: none;}" )
        self.place_edit.setFont( canda_12 )

        self.note_edit = QTextEdit(self)
        self.note_edit.setGeometry( 70, 165, 215, 80 )
        self.note_edit.setStyleSheet( "QTextEdit {color: rgba(125,125,125); background-color: rgba(29, 29, 29, 150); border: none;}" )
        self.note_edit.setFont( canda_12 )        
        
        self.save = QPushButton(self)
        self.save.setStyleSheet(qdim)
        self.save.setFont(canda_10)
        self.save.setText("SAVE")
        self.save.setGeometry(120, 295, 60, 50)
        self.save.clicked.connect(self.save)        
        
        self.exit = QPushButton(self)
        self.exit.setStyleSheet(qdim)
        self.exit.setFont(canda_10)
        self.exit.setText("EXIT")
        self.exit.setGeometry(210, 295, 60, 50)
        self.exit.clicked.connect(self.exit)
        
        self.savnexit = QPushButton(self)
        self.savnexit.setStyleSheet(qdim)
        self.savnexit.setFont(canda_10)
        self.savnexit.setText("SAVE\nEXIT")
        self.savnexit.setGeometry(10, 240, 281, 90)
        self.savnexit.clicked.connect(self.save_exit)


    def selectionchange(self):
        self.place_edit.setFocus()

    def paintEvent(self, e):
        self.painter = QPainter( self )
        self.painter.begin( self )
        self.painter.setPen(QColor(75, 75, 75))
        self.painter.drawLine(15, 65, 285, 65)
        self.painter.drawLine(15, 270, 285, 270 )
        self.painter.end()

    def repeat(self):
        date  = self.date_data.text()[-10:]
        time  = self.time_cbox.currentText()
        place = self.place_edit.text()
        note  = self.note_edit.toPlainText()
        coll.insert_one({'date': date, "time": time, 'place': place, 'note': note})

    def save(self):
        data = self.repeat()
        self.place_edit.clear()
        self.note_edit.clear()

    def save_exit(self):
        data = self.repeat()
        self.exit()

    def exit(self):
        self.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = EventForm()
    ex.show()
    sys.exit(app.exec_())
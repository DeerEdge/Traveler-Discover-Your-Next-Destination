import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit

save = False

def window():

    app = QApplication(sys.argv)
    widget = QWidget()

    lines = open('outputreport.txt').read()
    report = QLabel(widget)
    report.setText(lines)
    report.setWordWrap(True)
    report.move(64, 32)

    feedback = QLineEdit(widget)
    feedback.move(900, 300)
    feedback.textChanged.connect(save_text)
    global text
    text = feedback.text()

    button2 = QPushButton(widget)
    button2.setText("Send Feedback")
    button2.move(895, 325)
    button2.clicked.connect(button2_clicked)


    widget.setGeometry(50, 50, 320, 200)
    widget.setWindowTitle("Report")
    widget.show()
    sys.exit(app.exec_())

def button2_clicked(text):
    global save
    save = True

def save_text(text):
    global save

    if save == True:
        print(text[0:-1])
    save = False

if __name__ == '__main__':
    window()
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import mysql.connector as sqltor

mycon = sqltor.connect(host = "localhost", user = "student", passwd = "sairam", database = "test")
if mycon.is_connected():
    print("You have successfully connected to the database")
cursor = mycon.cursor()

class Ui_MainWindow(object):
    def check_and_submit(self):
        if self.lineEdit_2.text() == self.lineEdit_3.text() and "" not in [self.lineEdit.text(), self.lineEdit_2.text(), self.lineEdit_3.text()]:
           cursor.execute("INSERT INTO game_membership VALUES('" + self.lineEdit.text() + "', '" + self.lineEdit_2.text() + "', 'No');")
           mycon.commit()
           mycon.close()
           os.system("python LOGIN.py")
           app.quit()
        else:
            print("Please enter data in a proper manner.")
            return False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.resize(490, 466)
        MainWindow.setStyleSheet("\n"
"background-color: rgb(119, 255, 61);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(180, 20, 201, 41))
        self.label.setStyleSheet("color: rgb(255, 103, 15);\n"
"font: 26pt \"MS Gothic\";")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 110, 51, 21))
        self.label_2.setStyleSheet("color: rgb(255, 28, 8);\n"
"font: 18pt \"Segoe UI Historic\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 160, 71, 21))
        self.label_3.setStyleSheet("color: rgb(255, 28, 8);\n"
"font: 18pt \"Segoe UI Historic\";")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(60, 210, 131, 16))
        self.label_4.setStyleSheet("color: rgb(255, 28, 8);\n"
"font: 18pt \"Segoe UI Historic\";")
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(210, 260, 101, 31))
        self.pushButton.setStyleSheet("background-color:rgb(255, 14, 106);\n"
"color:rgb(243, 242, 255)")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.check_and_submit)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(210, 110, 113, 20))
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 160, 113, 20))
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(210, 210, 113, 20))
        self.lineEdit_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_3.setObjectName("lineEdit_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 490, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:36pt; font-weight:600;\">SIGN UP</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Name: </span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Password:</span></p><p><br/></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Confirm Password:</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "SUBMIT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

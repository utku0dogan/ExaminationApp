# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StudentEntryPage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_StudentEntry(object):
    def setupUi(self, StudentEntry):
        StudentEntry.setObjectName("StudentEntry")
        StudentEntry.resize(732, 704)
        self.calendar = QtWidgets.QCalendarWidget(StudentEntry)
        self.calendar.setGeometry(QtCore.QRect(160, 180, 411, 221))
        self.calendar.setObjectName("calendar")
        self.welcome_lbl = QtWidgets.QLabel(StudentEntry)
        self.welcome_lbl.setGeometry(QtCore.QRect(200, 60, 331, 61))
        font = QtGui.QFont()
        font.setFamily("Papyrus")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.welcome_lbl.setFont(font)
        self.welcome_lbl.setText("")
        self.welcome_lbl.setObjectName("welcome_lbl")
        self.pushButton = QtWidgets.QPushButton(StudentEntry)
        self.pushButton.setGeometry(QtCore.QRect(410, 460, 161, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(StudentEntry)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 460, 161, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(StudentEntry)
        self.pushButton_3.setGeometry(QtCore.QRect(160, 530, 161, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(StudentEntry)
        self.pushButton_4.setGeometry(QtCore.QRect(410, 530, 161, 41))
        self.pushButton_4.setObjectName("pushButton_4")

        self.retranslateUi(StudentEntry)
        QtCore.QMetaObject.connectSlotsByName(StudentEntry)

    def retranslateUi(self, StudentEntry):
        _translate = QtCore.QCoreApplication.translate
        StudentEntry.setWindowTitle(_translate("StudentEntry", "Ogrenci Giris Ekrani "))
        self.pushButton.setText(_translate("StudentEntry", "Zayıf konular sınav modülü"))
        self.pushButton_2.setText(_translate("StudentEntry", "6 sigma sınav modülü"))
        self.pushButton_3.setText(_translate("StudentEntry", "Istatistiklerim"))
        self.pushButton_4.setText(_translate("StudentEntry", "Ayarlar"))

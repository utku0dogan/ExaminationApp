# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dersEkle.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dersEkle(object):
    def setupUi(self, dersEkle):
        dersEkle.setObjectName("dersEkle")
        dersEkle.resize(498, 193)
        self.dersEkle_btn = QtWidgets.QPushButton(dersEkle)
        self.dersEkle_btn.setGeometry(QtCore.QRect(130, 110, 231, 51))
        self.dersEkle_btn.setObjectName("dersEkle_btn")
        self.lineEdit = QtWidgets.QLineEdit(dersEkle)
        self.lineEdit.setGeometry(QtCore.QRect(80, 20, 341, 61))
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(dersEkle)
        QtCore.QMetaObject.connectSlotsByName(dersEkle)

    def retranslateUi(self, dersEkle):
        _translate = QtCore.QCoreApplication.translate
        dersEkle.setWindowTitle(_translate("dersEkle", "Ders Ekle"))
        self.dersEkle_btn.setText(_translate("dersEkle", "Ekle"))

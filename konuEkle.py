# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'konuEkle.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addSection(object):
    def setupUi(self, addSection):
        addSection.setObjectName("addSection")
        addSection.setWindowModality(QtCore.Qt.NonModal)
        addSection.resize(470, 292)
        addSection.setFocusPolicy(QtCore.Qt.NoFocus)
        self.konuEkle_lbl = QtWidgets.QLabel(addSection)
        self.konuEkle_lbl.setGeometry(QtCore.QRect(30, 40, 211, 41))
        self.konuEkle_lbl.setObjectName("konuEkle_lbl")
        self.konEkle_cmb = QtWidgets.QComboBox(addSection)
        self.konEkle_cmb.setGeometry(QtCore.QRect(250, 50, 191, 22))
        self.konEkle_cmb.setObjectName("konEkle_cmb")
        self.konuEkle_txt = QtWidgets.QLineEdit(addSection)
        self.konuEkle_txt.setGeometry(QtCore.QRect(30, 110, 411, 51))
        self.konuEkle_txt.setObjectName("konuEkle_txt")
        self.konuEkle_btn = QtWidgets.QPushButton(addSection)
        self.konuEkle_btn.setGeometry(QtCore.QRect(30, 190, 411, 51))
        self.konuEkle_btn.setObjectName("konuEkle_btn")

        self.retranslateUi(addSection)
        QtCore.QMetaObject.connectSlotsByName(addSection)

    def retranslateUi(self, addSection):
        _translate = QtCore.QCoreApplication.translate
        addSection.setWindowTitle(_translate("addSection", "Konu Ekle"))
        self.konuEkle_lbl.setText(_translate("addSection", "konu (unite) eklenecek dersi seciniz"))
        self.konuEkle_btn.setText(_translate("addSection", "ekle"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'admin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_admin(object):
    def setupUi(self, admin):
        admin.setObjectName("admin")
        admin.resize(663, 507)
        self.tableWidget = QtWidgets.QTableWidget(admin)
        self.tableWidget.setGeometry(QtCore.QRect(120, 10, 411, 411))
        self.tableWidget.setLineWidth(0)
        self.tableWidget.setIconSize(QtCore.QSize(0, 0))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setObjectName("tableWidget")
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(49)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.pushButton = QtWidgets.QPushButton(admin)
        self.pushButton.setGeometry(QtCore.QRect(260, 430, 111, 41))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(admin)
        QtCore.QMetaObject.connectSlotsByName(admin)

    def retranslateUi(self, admin):
        _translate = QtCore.QCoreApplication.translate
        admin.setWindowTitle(_translate("admin", "admin"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("admin", "Qid"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("admin", "Question_Text"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("admin", "isActive"))
        self.pushButton.setText(_translate("admin", "degistir"))
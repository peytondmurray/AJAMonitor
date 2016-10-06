# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AJAMonitorGUI.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(983, 786)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plot1 = PlotWidget(self.centralwidget)
        self.plot1.setObjectName("plot1")
        self.verticalLayout.addWidget(self.plot1)
        self.plot2 = PlotWidget(self.centralwidget)
        self.plot2.setObjectName("plot2")
        self.verticalLayout.addWidget(self.plot2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setMinimumSize(QtCore.QSize(100, 100))
        self.startButton.setMaximumSize(QtCore.QSize(91, 81))
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setMinimumSize(QtCore.QSize(100, 100))
        self.clearButton.setMaximumSize(QtCore.QSize(91, 81))
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(88, 16))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.rateBox = QtWidgets.QSpinBox(self.centralwidget)
        self.rateBox.setMaximumSize(QtCore.QSize(79, 20))
        self.rateBox.setMaximum(999999999)
        self.rateBox.setProperty("value", 10)
        self.rateBox.setObjectName("rateBox")
        self.horizontalLayout.addWidget(self.rateBox)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 983, 21))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.clearButton.setText(_translate("MainWindow", "Clear"))
        self.label_2.setText(_translate("MainWindow", "Refresh rate (Hz):"))

from pyqtgraph import PlotWidget

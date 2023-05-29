# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtTinySpectrum.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setObjectName("tabWidget")
        self.analyserTab = QtWidgets.QWidget()
        self.analyserTab.setObjectName("analyserTab")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.analyserTab)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.controlgrid = QtWidgets.QGridLayout()
        self.controlgrid.setHorizontalSpacing(6)
        self.controlgrid.setObjectName("controlgrid")
        self.atten_box = QtWidgets.QSpinBox(self.analyserTab)
        self.atten_box.setMinimum(0)
        self.atten_box.setMaximum(31)
        self.atten_box.setProperty("value", 0)
        self.atten_box.setObjectName("atten_box")
        self.controlgrid.addWidget(self.atten_box, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.analyserTab)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.controlgrid.addWidget(self.label_4, 9, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.controlgrid.addItem(spacerItem, 19, 0, 1, 1)
        self.lna_button = QtWidgets.QPushButton(self.analyserTab)
        self.lna_button.setObjectName("lna_button")
        self.controlgrid.addWidget(self.lna_button, 2, 0, 1, 1)
        self.points_box = QtWidgets.QComboBox(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.points_box.sizePolicy().hasHeightForWidth())
        self.points_box.setSizePolicy(sizePolicy)
        self.points_box.setObjectName("points_box")
        self.controlgrid.addWidget(self.points_box, 6, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.analyserTab)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.controlgrid.addWidget(self.label_3, 7, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.analyserTab)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.controlgrid.addWidget(self.label_5, 0, 0, 1, 1)
        self.spur_button = QtWidgets.QPushButton(self.analyserTab)
        self.spur_button.setObjectName("spur_button")
        self.controlgrid.addWidget(self.spur_button, 14, 0, 1, 1)
        self.rbw_box = QtWidgets.QComboBox(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rbw_box.sizePolicy().hasHeightForWidth())
        self.rbw_box.setSizePolicy(sizePolicy)
        self.rbw_box.setEditable(True)
        self.rbw_box.setObjectName("rbw_box")
        self.controlgrid.addWidget(self.rbw_box, 8, 0, 1, 1)
        self.calc_box = QtWidgets.QComboBox(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calc_box.sizePolicy().hasHeightForWidth())
        self.calc_box.setSizePolicy(sizePolicy)
        self.calc_box.setObjectName("calc_box")
        self.controlgrid.addWidget(self.calc_box, 12, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.analyserTab)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.controlgrid.addWidget(self.label_2, 5, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.analyserTab)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.controlgrid.addWidget(self.label, 11, 0, 1, 1)
        self.vbw_box = QtWidgets.QComboBox(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.vbw_box.sizePolicy().hasHeightForWidth())
        self.vbw_box.setSizePolicy(sizePolicy)
        self.vbw_box.setObjectName("vbw_box")
        self.controlgrid.addWidget(self.vbw_box, 10, 0, 1, 1)
        self.gridLayout_3.addLayout(self.controlgrid, 0, 0, 1, 1)
        self.graphWidget = PlotWidget(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphWidget.sizePolicy().hasHeightForWidth())
        self.graphWidget.setSizePolicy(sizePolicy)
        self.graphWidget.setAutoFillBackground(False)
        self.graphWidget.setStyleSheet("")
        self.graphWidget.setObjectName("graphWidget")
        self.gridLayout_3.addWidget(self.graphWidget, 0, 2, 1, 1)
        self.freqgrid = QtWidgets.QGridLayout()
        self.freqgrid.setObjectName("freqgrid")
        self.stop_freq = QtWidgets.QDoubleSpinBox(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stop_freq.sizePolicy().hasHeightForWidth())
        self.stop_freq.setSizePolicy(sizePolicy)
        self.stop_freq.setDecimals(6)
        self.stop_freq.setMinimum(0.1)
        self.stop_freq.setMaximum(6000.0)
        self.stop_freq.setSingleStep(1.0)
        self.stop_freq.setProperty("value", 100.0)
        self.stop_freq.setObjectName("stop_freq")
        self.freqgrid.addWidget(self.stop_freq, 0, 6, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.freqgrid.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.freqgrid.addItem(spacerItem2, 0, 5, 1, 1)
        self.start_freq = QtWidgets.QDoubleSpinBox(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.start_freq.sizePolicy().hasHeightForWidth())
        self.start_freq.setSizePolicy(sizePolicy)
        self.start_freq.setPrefix("")
        self.start_freq.setDecimals(6)
        self.start_freq.setMinimum(0.1)
        self.start_freq.setMaximum(6000.0)
        self.start_freq.setSingleStep(1.0)
        self.start_freq.setProperty("value", 88.0)
        self.start_freq.setObjectName("start_freq")
        self.freqgrid.addWidget(self.start_freq, 0, 2, 1, 1)
        self.band_box = QtWidgets.QComboBox(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.band_box.sizePolicy().hasHeightForWidth())
        self.band_box.setSizePolicy(sizePolicy)
        self.band_box.setObjectName("band_box")
        self.freqgrid.addWidget(self.band_box, 0, 1, 1, 1)
        self.scan_button = QtWidgets.QPushButton(self.analyserTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scan_button.sizePolicy().hasHeightForWidth())
        self.scan_button.setSizePolicy(sizePolicy)
        self.scan_button.setCheckable(False)
        self.scan_button.setObjectName("scan_button")
        self.freqgrid.addWidget(self.scan_button, 0, 7, 1, 1)
        self.gridLayout_3.addLayout(self.freqgrid, 1, 2, 1, 1)
        self.tabWidget.addTab(self.analyserTab, "")
        self.generatorTab = QtWidgets.QWidget()
        self.generatorTab.setObjectName("generatorTab")
        self.label_6 = QtWidgets.QLabel(self.generatorTab)
        self.label_6.setGeometry(QtCore.QRect(30, 20, 58, 18))
        self.label_6.setObjectName("label_6")
        self.tabWidget.addTab(self.generatorTab, "")
        self.TimeTab = QtWidgets.QWidget()
        self.TimeTab.setEnabled(False)
        self.TimeTab.setObjectName("TimeTab")
        self.openGLWidget = GLViewWidget(self.TimeTab)
        self.openGLWidget.setGeometry(QtCore.QRect(240, 10, 756, 509))
        self.openGLWidget.setObjectName("openGLWidget")
        self.label_7 = QtWidgets.QLabel(self.TimeTab)
        self.label_7.setGeometry(QtCore.QRect(40, 30, 58, 18))
        self.label_7.setObjectName("label_7")
        self.tabWidget.addTab(self.TimeTab, "")
        self.gridLayout_4.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 23))
        self.menuBar.setObjectName("menuBar")
        self.menu_Help = QtWidgets.QMenu(self.menuBar)
        self.menu_Help.setObjectName("menu_Help")
        MainWindow.setMenuBar(self.menuBar)
        self.actionsetting = QtWidgets.QAction(MainWindow)
        self.actionsetting.setObjectName("actionsetting")
        self.actionlevel = QtWidgets.QAction(MainWindow)
        self.actionlevel.setObjectName("actionlevel")
        self.actionanother = QtWidgets.QAction(MainWindow)
        self.actionanother.setObjectName("actionanother")
        self.actionAbout_QtTinySA = QtWidgets.QAction(MainWindow)
        self.actionAbout_QtTinySA.setObjectName("actionAbout_QtTinySA")
        self.menu_Help.addAction(self.actionAbout_QtTinySA)
        self.menuBar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.points_box.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Qt TinySA"))
        self.atten_box.setSuffix(_translate("MainWindow", "dB"))
        self.label_4.setText(_translate("MainWindow", "VBW"))
        self.lna_button.setText(_translate("MainWindow", "LNA off"))
        self.label_3.setText(_translate("MainWindow", "RBW kHz"))
        self.label_5.setText(_translate("MainWindow", "Attenuator 0=auto"))
        self.spur_button.setText(_translate("MainWindow", "SPUR auto"))
        self.label_2.setText(_translate("MainWindow", "Points"))
        self.label.setText(_translate("MainWindow", "Trace Processing"))
        self.stop_freq.setSuffix(_translate("MainWindow", "MHz"))
        self.start_freq.setSuffix(_translate("MainWindow", "MHz"))
        self.scan_button.setText(_translate("MainWindow", "Run"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.analyserTab), _translate("MainWindow", "Analyser"))
        self.label_6.setText(_translate("MainWindow", "To Do"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generatorTab), _translate("MainWindow", "Generator"))
        self.label_7.setText(_translate("MainWindow", "To Do"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.TimeTab), _translate("MainWindow", "Time Spectrum"))
        self.menu_Help.setTitle(_translate("MainWindow", "&Help"))
        self.actionsetting.setText(_translate("MainWindow", "setting"))
        self.actionlevel.setText(_translate("MainWindow", "level"))
        self.actionanother.setText(_translate("MainWindow", "another"))
        self.actionAbout_QtTinySA.setText(_translate("MainWindow", "About QtTinySA"))
from pyqtgraph import PlotWidget
from pyqtgraph.opengl import GLViewWidget



import sys
import pyqtgraph as pg
from numpy import *
import AJAMonitorGUI
import time
from QueryDAQ import QueryDAQ
from DAQData import DAQData

from PyQt5 import QtGui, QtWidgets, QtCore


class AJAMonitorGUI(QtWidgets.QMainWindow, AJAMonitorGUI.Ui_MainWindow, object):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.connectButtons()
		self.setupDAQ()
		self.initializeData()
		self.makePens()
		self.decoratePlots()
		return

	def connectButtons(self):
		self.startButton.clicked.connect(self.start)
		self.clearButton.clicked.connect(self.clear)
		self.startButton.setStyleSheet("background-color: green")
		return

	def initializeData(self):
		maxlength = 1000
		self.ai0 = DAQData(maxlength)
		self.ai1 = DAQData(maxlength)
		self.ai2 = DAQData(maxlength)
		self.ai3 = DAQData(maxlength)
		return

	def setupDAQ(self):
		self.QueryDAQ = QueryDAQ()
		self.QueryDAQ.connectionError.connect(self.msg)
		self.QueryDAQ.dataReady.connect(self.updateGUI)
		return

	def start(self):
		self.QueryDAQ.setFreq(self.rateBox.value())
		self.startButton.setText("Stop")
		self.startButton.setStyleSheet("background-color: red")
		self.startButton.clicked.disconnect(self.start)
		self.startButton.clicked.connect(self.stop)
		self.QueryDAQ.start()
		return

	def stop(self):
		self.startButton.setText("Start")
		self.startButton.setStyleSheet("background-color: green")
		self.startButton.clicked.disconnect(self.stop)
		self.startButton.clicked.connect(self.start)
		self.QueryDAQ.stop()
		return

	def clear(self):
		self.ai0.clearData()
		self.ai1.clearData()
		self.ai2.clearData()
		self.ai3.clearData()
		self.clearPlots()
		return

	def msg(self, text):
		self.statusBar().showMessage(text, 5000)
		return

	def updateGUI(self, d_ai0, d_ai1, d_ai2, d_ai3):
		self.updateData(d_ai0, d_ai1, d_ai2, d_ai3)
		self.clearPlots()
		self.plotData()
		self.repaintPlots()
		return

	def updateData(self, d_ai0, d_ai1, d_ai2, d_ai3):
		self.ai0.addData(d_ai0)
		self.ai1.addData(d_ai1)
		self.ai2.addData(d_ai2)
		self.ai3.addData(d_ai3)
		return

	def clearPlots(self):
		self.plot1_V.clear()
		self.plot1_I.clear()
		self.plot2_V.clear()
		self.plot2_I.clear()
		return

	def makePens(self):
		self.wpen = pg.mkPen(color='w')
		self.rpen = pg.mkPen(color='r')
		self.wbrush = pg.mkBrush(color='w')
		self.rbrush = pg.mkBrush(color='r')

	def decoratePlots(self):
		self.plot1_V = self.plot1.getPlotItem()						# Get the plotItem in self.plot
		self.plot1_I = pg.ViewBox()									# Make a new ViewBox to draw stuff into
		self.plot1_I_axis = pg.AxisItem('right', pen=self.rpen)  	# Make a new AxisItem for plotting

		self.plot1_V.layout.addItem(self.plot1_I_axis, 2, 3)  		# Add the new AxisItem to the old plotItem layout
		self.plot1_V.scene().addItem(self.plot1_I)  				# Add the new ViewBox to the old plotItem scene
		self.plot1_I_axis.linkToView(self.plot1_I)  				# Link the new Axis to the new ViewBox
		self.plot1_I.setXLink(self.plot1_V)  						# Link the axes of the new ViewBox to the original plotItem
		self.plot1_I_axis.setLabel("Current", units="A")
		self.plot1_V.setLabel('left', "Voltage", "V")
		self.plot1_V.setLabel('bottom', "Time", 's')
		self.plot1.setTitle("MDX 500: DC1")

		self.plot2_V = self.plot2.getPlotItem()  				# Get the plotItem in self.plot2
		self.plot2_I = pg.ViewBox()  							# Make a new ViewBox to draw stuff into
		self.plot2_I_axis = pg.AxisItem('right', pen=self.rpen) # Make a new AxisItem for plotting

		self.plot2_V.layout.addItem(self.plot2_I_axis, 2, 3)  	# Add the new AxisItem to the old plotItem layout
		self.plot2_V.scene().addItem(self.plot2_I)  			# Add the new ViewBox to the old plotItem scene
		self.plot2_I_axis.linkToView(self.plot2_I)  			# Link the new Axis to the new ViewBox
		self.plot2_I.setXLink(self.plot2_V)  					# Link the axes of the new ViewBox to the original plotItem
		self.plot2_I_axis.setLabel("Current", units="A")
		self.plot2_V.setLabel('left', "Voltage", "V")
		self.plot2_V.setLabel('bottom', "Time", 's')
		self.plot2.setTitle("MDX 500: DC2")

		self.updateViews()
		self.plot1_V.vb.sigResized.connect(self.updateViews)
		self.plot2_V.vb.sigResized.connect(self.updateViews)

		self.repaintPlots()

		return

	def updateViews(self):
		self.plot1_I.setGeometry(self.plot1_V.vb.sceneBoundingRect())
		self.plot1_I.linkedViewChanged(self.plot1_V.vb, self.plot1_I.XAxis)
		self.plot2_I.setGeometry(self.plot2_V.vb.sceneBoundingRect())
		self.plot2_I.linkedViewChanged(self.plot2_V.vb, self.plot2_I.XAxis)
		return

	def rerangePlots(self):
		self.plot1_V.setRange(xRange=self.ai0.getXlim(), yRange=self.ai0.getYlim())
		self.plot1_I.setRange(yRange=self.ai1.getYlim())
		self.plot2_V.setRange(xRange=self.ai2.getXlim(), yRange=self.ai2.getYlim())
		self.plot_I.setRange(yRange=self.ai3.getYlim())
		return

	def repaintPlots(self):
		self.plot1.repaint()
		self.plot2.repaint()
		return

	def plotData(self):
		self.plot1_V.addItem(pg.PlotDataItem(x=self.ai0.getXdata(), y=self.ai0.getYdata(), pen=self.wpen, symbol=None, symbolPen=self.wpen, symbolBrush=self.wbrush, pxMode=True))
		self.plot1_I.addItem(pg.PlotDataItem(x=self.ai1.getXdata(), y=self.ai1.getYdata(), pen=self.rpen, symbol=None, symbolPen=self.rpen, symbolBrush=self.rbrush, pxMode=True))
		self.plot2_V.addItem(pg.PlotDataItem(x=self.ai2.getXdata(), y=self.ai2.getYdata(), pen=self.wpen, symbol=None, symbolPen=self.wpen, symbolBrush=self.wbrush, pxMode=True))
		self.plot2_I.addItem(pg.PlotDataItem(x=self.ai3.getXdata(), y=self.ai3.getYdata(), pen=self.rpen, symbol=None, symbolPen=self.rpen, symbolBrush=self.rbrush, pxMode=True))
		return



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	win = AJAMonitorGUI()
	win.setWindowTitle("AJAMonitorGUI")
	win.show()
	sys.exit(app.exec_())

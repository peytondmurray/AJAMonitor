import sys
import visa
import pyqtgraph as pg
from numpy import *
import QueryDAQ
import AJAMonitorGUI
import time
from labjack import u12

from PyQt5 import QtGui, QtWidgets, QtCore


class AJAMonitorGUI(QtWidgets.QMainWindow, AJAMonitorGUI.Ui_MainWindow, object):

	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.connectButtons()
		self.xdata_DC1 = []
		self.xdata_DC2 = []
		self.ydata_ai0 = []
		self.ydata_ai1 = []
		self.ydata_ai2 = []
		self.ydata_ai3 = []

		self.threshold_V = 10
		self.threshold_I = 0.10

		self.wpen = pg.mkPen(color='w')
		self.rpen = pg.mkPen(color='r')
		self.wbrush = pg.mkBrush(color='w')
		self.rbrush = pg.mkBrush(color='r')

		self.decoratePlot()
		return

	def connectButtons(self):
		self.startButton.clicked.connect(self.startButtonClicked)
		self.stopButton.clicked.connect(self.stopButtonClicked)
		self.clearButton.clicked.connect(self.clearButtonClicked)
		self.refreshButton.clicked.connect(self.refreshButtonClicked)

		self.refreshButtonClicked()
		return

	def startButtonClicked(self):
		self.t0 = time.time()
		self.daq = QueryDAQ.QueryDAQ(u12.U12(), freq=self.rateBox.value())
		self.daq.dataReady.connect(self.updatePlot)
		self.daq.start()
		self.startButton.setEnabled(False)
		return

	def stopButtonClicked(self):
		# self.queryThread.stop()
		self.daq.stop()
		self.startButton.setEnabled(True)
		return

	def clearButtonClicked(self):
		self.xdata_DC1 = []
		self.xdata_DC2 = []
		self.ydata_ai0 = []
		self.ydata_ai1 = []
		self.ydata_ai2 = []
		self.ydata_ai3 = []

		self.plot_V.clear()
		self.plot_I.clear()
		self.plot2_V.clear()
		self.plot2_I.clear()

		self.statusBar.showMessage("Data entries stored: {}".format(sum(list(map(len, [self.xdata_DC1, self.xdata_DC2, self.ydata_ai0, self.ydata_ai1, self.ydata_ai2, self.ydata_ai3])))))
		return

	def refreshButtonClicked(self):
		self.gpibBox.clear()
		instruments = visa.ResourceManager().list_resources()
		self.gpibBox.addItems(instruments)
		return

	def decoratePlot(self):
		self.plot_V = self.plot.getPlotItem()								#Get the plotItem in self.plot
		self.plot_I = pg.ViewBox()											#Make a new ViewBox to draw stuff into
		self.plot_I_axis = pg.AxisItem('right', pen=self.rpen)				#Make a new AxisItem for plotting

		self.plot_V.layout.addItem(self.plot_I_axis, 2, 3)					#Add the new AxisItem to the old plotItem layout
		self.plot_V.scene().addItem(self.plot_I)							#Add the new ViewBox to the old plotItem scene
		self.plot_I_axis.linkToView(self.plot_I)  # Link the new Axis to the new ViewBox
		self.plot_I.setXLink(self.plot_V)									#Link the axes of the new ViewBox to the original plotItem
		self.plot_I_axis.setLabel("Current", units="A")
		self.plot_V.setLabel('left', "Voltage", "V")
		self.plot_V.setLabel('bottom', "Time", 's')
		self.plot.setTitle("MDX 500: DC1")


		self.plot2_V = self.plot2.getPlotItem()								#Get the plotItem in self.plot2
		self.plot2_I = pg.ViewBox()											#Make a new ViewBox to draw stuff into
		self.plot2_I_axis = pg.AxisItem('right', pen=self.rpen)				#Make a new AxisItem for plotting

		self.plot2_V.layout.addItem(self.plot2_I_axis, 2, 3)				#Add the new AxisItem to the old plotItem layout
		self.plot2_V.scene().addItem(self.plot2_I)							#Add the new ViewBox to the old plotItem scene
		self.plot2_I_axis.linkToView(self.plot2_I)  # Link the new Axis to the new ViewBox
		self.plot2_I.setXLink(self.plot2_V)  # Link the axes of the new ViewBox to the original plotItem
		self.plot2_I_axis.setLabel("Current", units="A")
		self.plot2_V.setLabel('left', "Voltage", "V")
		self.plot2_V.setLabel('bottom', "Time", 's')
		self.plot2.setTitle("MDX 500: DC2")

		self.updateViews()
		self.plot_V.vb.sigResized.connect(self.updateViews)
		self.plot2_V.vb.sigResized.connect(self.updateViews)

		self.plot.repaint()
		self.plot2.repaint()
		self.plot3.repaint()
		return

	def updatePlot(self, ai0, ai1, ai2, ai3):
		self.clearPlots()
		self.appendData(time.time()-self.t0, ai0, ai1, ai2, ai3)
		# self.rerangePlots()
		self.plotData()
		self.repaintPlots()
		return

	def clearPlots(self):
		self.plot_V.clear()
		self.plot2_V.clear()
		self.plot_I.clear()
		self.plot2_I.clear()
		# self.plot3.clear()
		return

	def appendData(self, t, ai0, ai1, ai2, ai3):


		if ai0 > self.threshold_V and ai1 > self.threshold_I:
			self.ydata_ai0.append(ai0)
			self.ydata_ai1.append(ai1)
			self.xdata_DC1.append(time.time() - self.t0)
		if ai2 > self.threshold_V and ai3 > self.threshold_I:
			self.ydata_ai2.append(ai2)
			self.ydata_ai3.append(ai3)
			self.xdata_DC2.append(time.time() - self.t0)
		self.statusBar.showMessage("Data entries stored: {}".format(sum(list(map(len, [self.xdata_DC1, self.xdata_DC2, self.ydata_ai0, self.ydata_ai1, self.ydata_ai2, self.ydata_ai3])))))
		return

	def rerangePlots(self):
		self.plot_V.setRange(xRange=[self.xdata_DC1[0], self.xdata_DC1[-1]], yRange=[min(self.ydata_ai0), max(self.ydata_ai0)])
		self.plot_I.setRange(yRange=[min(self.ydata_ai1), max(self.ydata_ai1)])
		self.plot2_V.setRange(xRange=[self.xdata_DC2[0], self.xdata_DC2[-1]], yRange=[min(self.ydata_ai2), max(self.ydata_ai2)])
		self.plot_I.setRange(yRange=[min(self.ydata_ai3), max(self.ydata_ai3)])
		return

	def plotData(self):
		self.plot_V.addItem(pg.PlotDataItem(x=self.xdata_DC1, y=self.ydata_ai0, pen=self.wpen, symbol='o', symbolPen=self.wpen, symbolBrush=self.wbrush, pxMode=True))
		self.plot_I.addItem(pg.PlotDataItem(x=self.xdata_DC1, y=self.ydata_ai1, pen=self.rpen, symbol='o', symbolPen=self.rpen,symbolBrush=self.rbrush, pxMode=True))
		self.plot2_V.addItem(pg.PlotDataItem(x=self.xdata_DC2, y=self.ydata_ai2, pen=self.wpen, symbol='o', symbolPen=self.wpen, symbolBrush=self.wbrush, pxMode=True))
		self.plot2_I.addItem(pg.PlotDataItem(x=self.xdata_DC2, y=self.ydata_ai3, pen=self.rpen, symbol='o', symbolPen=self.rpen, symbolBrush=self.rbrush, pxMode=True))
		return

	def repaintPlots(self):
		self.plot.repaint()
		self.plot2.repaint()
		self.plot3.repaint()
		return

	def updateViews(self):
		self.plot_I.setGeometry(self.plot_V.vb.sceneBoundingRect())
		self.plot_I.linkedViewChanged(self.plot_V.vb, self.plot_I.XAxis)
		self.plot2_I.setGeometry(self.plot2_V.vb.sceneBoundingRect())
		self.plot2_I.linkedViewChanged(self.plot2_V.vb, self.plot2_I.XAxis)
		return


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	win = AJAMonitorGUI()
	win.setWindowTitle("AJAMonitorGUI")
	win.show()
	sys.exit(app.exec_())

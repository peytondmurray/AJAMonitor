
#Holds a single channel's data

from time import time
import numpy as np

class DAQData:

	def __init__(self, maxlength):
		self.timedata = np.array([])
		self.ydata = np.array([])
		self.maxlength = maxlength
		return

	def addData(self, value):
		if len(self.timedata) == 0:
			self.t0 = time()
		elif len(self.timedata) > self.maxlength:
			self.thinData()

		self.timedata = np.append(self.timedata, time()-self.t0)
		self.ydata = np.append(self.ydata, value)

		return

	def getData(self):
		return self.timedata, self.ydata

	def getXdata(self):
		return self.timedata

	def getYdata(self):
		return self.ydata

	def clearData(self):
		self.timedata = np.array([])
		self.ydata = np.array([])
		return

	def getXlim(self):
		return [min(self.timedata), max(self.timedata)]

	def getYlim(self):
		return [min(self.ydata), max(self.ydata)]

	def thinData(self):
		return



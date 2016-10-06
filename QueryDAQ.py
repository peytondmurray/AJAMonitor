

from Reader import MultiChannelAnalogInput
from PyQt5.QtCore import QThread, pyqtSignal

class QueryDAQ(QThread):

	dataReady = pyqtSignal(float, float, float, float)
	connectionError = pyqtSignal(str)

	def __init__(self):
		super().__init__()

		#Calibration constants for the different MDX500 power supplies
		self.Vcal = 120
		self.Ical = 0.1
		self.Pcal = 50

		try:
			self.DAQ = MultiChannelAnalogInput(["Dev1/ai0", "Dev1/ai1", "Dev1/ai2", "Dev1/ai3"])
			self.DAQ.configure()
		except:
			self.connectionError.emit("Issue connecting.")

		self.stopFlag = False
		return

	def __del__(self):
		self.wait()

	def stop(self):
		self.stopFlag = True

	def run(self):
		self.stopFlag = False
		while not self.stopFlag:
			self.dataReady.emit(self.Vcal*float(self.DAQ.read(0)), self.Ical*float(self.DAQ.read(1)), self.Vcal*float(self.DAQ.read(2)), self.Ical*float(self.DAQ.read(3)))
			self.msleep(1000/self.freq)

	def setFreq(self, freq):
		self.freq = freq
		return
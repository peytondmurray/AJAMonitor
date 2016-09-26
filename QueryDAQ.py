from PyQt5 import QtCore

class QueryDAQ(QtCore.QThread):

	dataReady = QtCore.pyqtSignal(float, float, float, float)

	def __init__(self, device, freq):
		QtCore.QThread.__init__(self)
		self.calibration_V = 120
		self.calibration_I = 0.1
		self.calibration_P = 50

		self.device = device
		self.channels = [0, 1, 2, 3]
		self.rate = 1/freq
		self.stopFlag = False

	def __del__(self):
		self.wait()

	def run(self):
		while not self.stopFlag:
			outputs = list(map(self.device.eAnalogIn, self.channels))
			voltages = self.calibration_V*outputs[0]['voltage'], self.calibration_I*outputs[1]['voltage'], self.calibration_V*outputs[2]['voltage'], self.calibration_I*outputs[3]['voltage']
			self.dataReady.emit(*voltages)
			self.msleep(1000*self.rate)
		return

	def stop(self):
		self.stopFlag = True
		return
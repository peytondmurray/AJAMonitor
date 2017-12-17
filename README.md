# AJAMonitor
Monitors AJA Sputter Deposition Conditions

This program uses a NI USB-DAQ board to read output voltages from our AE MDX-500 power supplies, which power our sputter guns. I wanted to be able to monitor the current and voltage before and during deposition. There are two buttons: start/stop, and clear. There's also a box which controls the read rate. It's pretty simple to use.

The GUI uses PyQt for the interface with pyqtgraph for the plots.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Originally created on Tue 1 May 2023 @author: Ian Jefferson G4IXT
TinySA Ultra GUI programme using Qt5 and PyQt.

This code attempts to replicate some of the TinySA Ultra on-screen commands and to provide PC control.
Development took place on Kubuntu 22.04LTS with Python 3.9 and PyQt5 using Spyder in Anaconda.
Not tested in any Windows version.

TinySA and TinySA Ultra are trademarks of Erik Kaashoek and are used with permission.

TinySA commands are based on Erik's Python examples:
http://athome.kaashoek.com/tinySA/python/

The serial communication commands are based on the Python NanoVNA/TinySA Toolset of Martin Ho-Ro:
https://github.com/Ho-Ro

"""

import time
import logging
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QRunnable, QObject, QThreadPool
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import pyqtgraph
import QtTinySpectrum  # the GUI
import struct
import serial
from serial.tools import list_ports

#  For 3D
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as pyqtgl
#  3D

logging.basicConfig(format="%(message)s", level=logging.INFO)

threadpool = QThreadPool()

# TinySA Ultra hardware ID
VID = 0x0483  # 1155
PID = 0x5740  # 22336

# amateur frequency band values
fBandStart = [1.8, 3.5, 7.0, 10.1, 14.0, 18.068, 21.0, 24.89, 28.0,
              50.0, 70.0, 144.0, 430.0, 1240, 2300, 2390, 3300, 5650]
fBandStop = [2.0, 3.8, 7.1, 10.15, 14.35, 18.168, 21.45, 24.99, 29.7,
             52.0, 70.5, 146.0, 440.0, 1325, 2310, 2450, 3500, 5925]
bands = list(map(str, fBandStart))  # convert start freq float list to string list for GUI combobox
bands = [freq + ' MHz' for freq in bands]
bands.insert(0, 'Band')

# pyqtgraph pens
red = pyqtgraph.mkPen(color='r', width=1.0)
yellow = pyqtgraph.mkPen(color='y', width=1.0)
white = pyqtgraph.mkPen(color='w', width=1.0)
cyan = pyqtgraph.mkPen(color='c', width=1.0)
red_dash = pyqtgraph.mkPen(color='r', width=0.5, style=QtCore.Qt.DashLine)
blue_dash = pyqtgraph.mkPen(color='b', width=0.5,  style=QtCore.Qt.DashLine)

###############################################################################
# classes


class analyser:
    def __init__(self, dev=None):
        self.dev = getport()
        self._frequencies = None
        self.sweeping = False
        self.signals = WorkerSignals()
        self.signals.result.connect(self.sigProcess)
        self.timeout = 1
        self.scanCount = 0
        self.runTimer = QtCore.QElapsedTimer()

    @property
    def frequencies(self):
        # what does this do?
        return self._frequencies

    def startMeasurement(self, startF, stopF):
        self.sweep = Worker(self.measurement, startF, stopF)  # workers are auto-deleted when thread stops
        self.sweeping = True
        self.sweepresults = np.full((self.points, self.points), -100, dtype=float)  # to do - add row count to GUI
        tinySA.createTimeSpectrum()
        threadpool.start(self.sweep)

    def serialSend(self, command):
        self.clearBuffer()
        with serial.Serial(port=self.dev, baudrate=3000000) as SA:  # baudrate does nothing for USB cnx
            SA.timeout = 1
            logging.debug(command)
            SA.write(command)
            SA.read_until(b'ch> ')  # skip command echo and prompt

    def set_frequencies(self, startF, stopF, points):  # needs update
        # creates a np array of equi-spaced freqs in Hz (but doesn't set it on the tinySA)
        self.points = points
        self._frequencies = np.linspace(startF, stopF, self.points, dtype=int)
        logging.debug(f'frequencies = {self._frequencies}')

    def setRBW(self):
        if ui.rbw_box.currentIndex == 0:
            self.rbw = 'auto'
        else:
            self.rbw = ui.rbw_box.currentText()  # ui values are discrete ones in kHz
        rbw_command = f'rbw {self.rbw}\r'.encode()
        self.serialSend(rbw_command)

    def clearBuffer(self):
        with serial.Serial(self.dev, baudrate=3000000) as serialPort:  # baudrate does nothing for USB cnx
            serialPort.timeout = 1
            while serialPort.inWaiting():
                serialPort.read_all()  # keep the serial buffer clean
                time.sleep(0.1)

    def sweepTimeout(self, f_low, f_high):  # freqs are in Hz
        if self.rbw == 'auto':
            rbw = (f_high / 1e3 - f_low / 1e3) / self.points  # rbw equal to freq step size in kHz
        else:
            rbw = float(self.rbw)

        if rbw < 0.2:  # change this to something more fancy
            rbw = 0.2
        elif rbw > 850:
            rbw = 850

        # timeout can be very long - use a heuristic approach
        timeout = int(((f_high - f_low) / 1e3) / (rbw ** 2) + self.points / 1e3) + 5
        self.timeout = timeout
        logging.debug(f'sweepTimeout = {self.timeout}')

    # return 1D numpy array with power as dBm.  Freqs are in Hz
    def measurement(self, f_low, f_high):  # runs in a separate thread
        self.threadrunning = True
        while self.sweeping:
            with serial.Serial(self.dev, baudrate=3000000) as serialPort:  # baudrate does nothing for USB cnx
                serialPort.timeout = self.timeout
                logging.debug(f'serial timeout: {self.timeout} s\n')
                logging.debug(f'points: {self.points} s\n')
                scan_command = f'scanraw {int(f_low)} {int(f_high)} {int(self.points)}\r'.encode()
                serialPort.write(scan_command)
                serialPort.read_until(b'{')  # skip command echoes
                raw_data = serialPort.read_until(b'}ch> ')
            raw_data = struct.unpack('<' + 'xH'*self.points, raw_data[:-5])  # ignore trailing '}ch> '
            raw_data = np.array(raw_data, dtype=np.uint16)
            logging.debug(f'raw data: {raw_data} s\n')
            SCALE = 174  # tinySA: 128  tinySA4: 174
            dBm_power = (raw_data / 32) - SCALE  # scale 0..4095 -> -128..-0.03 dBm
            # store each sweep in an array with most recent at index 0
            self.sweepresults = np.roll(self.sweepresults, 1, axis=0)
            self.sweepresults[0] = dBm_power
            self.signals.result.emit(self.sweepresults)
        self.threadrunning = False

#    def battery():
        # command = 'vbat\r'.encode()
        # need to get data

    def sigProcess(self, signaldBm):  # signaldBm is emitted from the worker thread
        signalAvg = np.average(signaldBm[:ui.avgSlider.value(), ::], axis=0)
        signalMax = np.amax(signaldBm[:100, ::], axis=0)
        signalMin = np.amin(signaldBm[:100, ::], axis=0)
        options = {'Normal': signaldBm[0], 'Average': signalAvg, 'Max': signalMax, 'Min': signalMin}
        spectrum1.updateGUI(options.get(spectrum1.traceType))
        spectrum2.updateGUI(options.get(spectrum2.traceType))
        spectrum3.updateGUI(options.get(spectrum3.traceType))
        spectrum4.updateGUI(options.get(spectrum4.traceType))

        # self.updateTimeSpectrum()

    def createTimeSpectrum(self):
        # x = self.frequencies / 1e7
        x = np.arange(start=self.points, stop=0, step=-1)
        y = np.arange(start=0, stop=self.points)  # this is the spectrum measurement depth
        z = self.sweepresults
        logging.debug(f'z = {z}')
        self.p2 = pyqtgl.GLSurfacePlotItem(x=x, y=y, z=z, shader='normalColor')
        self.p2.translate(-10, -10, 0)
        self.p2.setDepthValue(-120)
        ui.openGLWidget.addItem(self.p2)

    def updateTimeSpectrum(self):
        z = self.sweepresults
        logging.info(f'z = {z}')
        self.p2.setData(z=z)

    def pause(self):
        # pauses the sweeping in either input or output mode
        pause_command = 'pause\r'.encode()
        self.serialSend(pause_command)

    def resume(self):
        # resumes the sweeping in either input or output mode
        resume_command = 'resume\r'.encode()
        self.serialSend(resume_command)

    def initialise(self):
        command = 'spur auto\r'.encode()
        tinySA.serialSend(command)
        self.spur_auto = True
        command = 'lna off\r'.encode()
        tinySA.serialSend(command)
        self.lna_on = False


class display:
    def __init__(self, name):
        self.trace = ui.graphWidget.plot([], [], name=name, pen=yellow, width=1)
        self.traceType = 'Normal'  # Normal, Average, Max, Min
        self.markerType = 'Normal'  # Normal, Delta; Peak
        self.vline = ui.graphWidget.addLine(88, 90, movable=True, pen=pyqtgraph.mkPen('g', width=0.5, style=QtCore.Qt.DashLine), label="{value:.2f}")
        self.hline = ui.graphWidget.addLine(-100, 0, movable=False, pen=pyqtgraph.mkPen('g', width=0.5, style=QtCore.Qt.DashLine),  label="{value:.2f}")
        self.hline.setAngle(0)
        self.vline.hide()
        self.hline.hide()
        self.fIndex = 0  # index of current marker freq in frequencies array
        self.dIndex = 0

    def setDiscrete(self):
        # update marker to discrete freq point nearest, if it's within the sweep range
        if self.vline.value() >= ui.start_freq.value() and self.vline.value() <= ui.stop_freq.value():
            try:
                for i in range(tinySA.points):
                    if tinySA.frequencies[i] / 1e6 >= self.vline.value():
                        self.vline.setValue(tinySA.frequencies[i] / 1e6)
                        self.hline.setValue(float(tinySA.sweepresults[0, i]))
                        self.fIndex = i
                        if self.markerType == 'Delta':
                            self.dIndex = self.fIndex - spectrum1.fIndex
                        return
            except AttributeError:
                return

    def mStart(self):
        # set marker to the sweep start frequency
        self.fIndex = 0
        self.vline.setValue(ui.start_freq.value())

    def mType(self, uiBox):
        self.markerType = uiBox.currentText()
        self.dIndex = self.fIndex - spectrum1.fIndex
        logging.debug(f'marker = type {self.markerType}')

    def tType(self, uiBox):
        self.traceType = uiBox.currentText()

    def enableMarker(self, mkr):
        if mkr.isChecked():
            self.vline.show()
            self.hline.show()
        else:
            self.vline.hide()
            self.hline.hide()

    def updateGUI(self, signal):
        self.trace.setData((tinySA.frequencies/1e6), signal)
        self.hline.setValue(signal[self.fIndex])  # set to dBm value at marker freq


class WorkerSignals(QObject):
    error = pyqtSignal(str)
    result = pyqtSignal(np.ndarray)
    finished = pyqtSignal()


class Worker(QRunnable):
    '''Worker threads so that functions can run outside GUI event loop'''

    def __init__(self, fn, *args):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''Initialise the runner'''
        logging.info(f'{self.fn.__name__} thread running')
        self.fn(*self.args)
        logging.info(f'{self.fn.__name__} thread stopped')


###############################################################################
# other methods

# Get tinysa device automatically
def getport() -> str:
    try:
        device_list = list_ports.comports()
    except serial.SerialException:
        logging.info('serial exception')
    for x in device_list:
        if x.vid == VID and x.pid == PID:
            return x.device
    raise OSError("TinySA not found")


def scan():
    if tinySA.sweeping:  # if it's running, stop it
        tinySA.sweeping = False  # tells the measurement thread to stop once current scan complete
        ui.scan_button.setEnabled(False)  # prevent repeat presses of 'stop'
        while tinySA.threadrunning:
            time.sleep(0.1)  # wait until the measurement thread stops using the serial comms
        ui.scan_button.setEnabled(True)
        activeButtons(True)
        ui.scan_button.setText('Run')  # toggle the 'Stop' button text
        # tinySA.updateTimeSpectrum()
    else:
        tinySA.pause()
        startF = ui.start_freq.value()*1e6
        stopF = ui.stop_freq.value()*1e6
        points = int(ui.points_box.currentText())
        tinySA.set_frequencies(startF, stopF, points)
        tinySA.setRBW()  # fetches rbw value from the GUI combobox and sends it to TinySA
        tinySA.clearBuffer()
        tinySA.sweepTimeout(startF, stopF)
        activeButtons(False)
        ui.scan_button.setText('Stop')  # toggle the 'Run' button text
        app.processEvents()
        tinySA.startMeasurement(startF, stopF)  # runs measurement in separate thread


def rbw_changed():
    tinySA.setRBW()


def start_freq_changed():
    ui.band_box.setCurrentIndex(0)
    start = ui.start_freq.value()
    stop = ui.stop_freq.value()
    if start > stop:
        ui.stop_freq.setValue(start)
        stop = start
        stop_freq_changed()
    ui.graphWidget.setXRange(start, stop)

    command = f'sweep start {start * 1e6}\r'.encode()
    tinySA.serialSend(command)


def stop_freq_changed():
    ui.band_box.setCurrentIndex(0)
    start = ui.start_freq.value()
    stop = ui.stop_freq.value()
    if start > stop:
        ui.start_freq.setValue(stop)
        start = stop
        start_freq_changed()
    ui.graphWidget.setXRange(start, stop)

    command = f'sweep stop {stop * 1e6}\r'.encode()
    tinySA.serialSend(command)


def band_changed():
    index = ui.band_box.currentIndex()
    if index == 0:
        return
    else:
        index -= 1
        start = fBandStart[index]
        ui.start_freq.setValue(start)
        start_freq_changed()
        stop = fBandStop[index]
        ui.stop_freq.setValue(stop)
        stop_freq_changed()


def attenuate_changed():  # lna and attenuator are switched so mutually exclusive. To do: add code for this
    atten = ui.atten_box.value()
    if atten == 0:
        atten = 'auto'
    command = f'attenuate {str(atten)}\r'.encode()
    tinySA.serialSend(command)


def spur():
    if tinySA.spur_auto:
        command = 'spur off\r'.encode()
        tinySA.spur_auto = False
        ui.spur_button.setText('SPUR off')
    else:
        command = 'spur auto\r'.encode()
        tinySA.spur_auto = True
        ui.spur_button.setText('SPUR auto')
    tinySA.serialSend(command)


def lna():  # lna and attenuator are switched so mutually exclusive. To do: add code for this
    if tinySA.lna_on:
        command = 'lna off\r'.encode()
        tinySA.lna_on = False
        ui.lna_button.setText('LNA off')
    else:
        command = 'lna on\r'.encode()
        tinySA.lna_on = True
        ui.lna_button.setText('LNA on')
    tinySA.serialSend(command)


def mStart():
    if ui.marker1.isChecked():
        spectrum1.mStart()
    if ui.marker2.isChecked():
        spectrum2.mStart()
    if ui.marker3.isChecked():
        spectrum3.mStart()
    if ui.marker4.isChecked():
        spectrum4.mStart()


def mkr1_moved():
    spectrum1.vline.sigPositionChanged.connect(spectrum1.setDiscrete)
    try:
        if spectrum2.markerType == 'Delta':
            spectrum2.fIndex = spectrum1.fIndex + spectrum2.dIndex
            spectrum2.vline.setValue(tinySA.frequencies[spectrum2.fIndex] / 1e6)
        if spectrum3.markerType == 'Delta':
            spectrum3.fIndex = spectrum1.fIndex + spectrum3.dIndex
            spectrum3.vline.setValue(tinySA.frequencies[spectrum3.fIndex] / 1e6)
        if spectrum4.markerType == 'Delta':
            spectrum4.fIndex = spectrum1.fIndex + spectrum4.dIndex
            spectrum4.vline.setValue(tinySA.frequencies[spectrum4.fIndex] / 1e6)
    except IndexError:
        popUp('Delta Marker out of bounds', 'ok')


def exit_handler():
    tinySA.sweeping = False
    time.sleep(1)  # allow time for measurements to stop
    tinySA.resume()
    app.processEvents()
    logging.info('Closed')


def popUp(message, button):
    msg = QMessageBox(parent=(window))
    msg.setIcon(QMessageBox.Warning)
    msg.setText(message)
    msg.addButton(button, QMessageBox.ActionRole)
    msg.exec_()


##############################################################################
# respond to GUI signals


def activeButtons(tF):
    # disable/enable buttons that send commands to TinySA (Because Comms are in use if scanning)
    ui.atten_box.setEnabled(tF)
    ui.spur_button.setEnabled(tF)
    ui.lna_button.setEnabled(tF)
    ui.rbw_box.setEnabled(tF)
    ui.vbw_box.setEnabled(tF)
    ui.points_box.setEnabled(tF)
    ui.band_box.setEnabled(tF)
    ui.start_freq.setEnabled(tF)
    ui.stop_freq.setEnabled(tF)


###############################################################################
# Instantiate classes

tinySA = analyser(getport())
app = QtWidgets.QApplication([])  # create QApplication for the GUI
window = QtWidgets.QMainWindow()
ui = QtTinySpectrum.Ui_MainWindow()
ui.setupUi(window)

# Traces & markers
spectrum1 = display(1)
spectrum2 = display(2)
spectrum2.trace.setPen(red)
spectrum3 = display(3)
spectrum3.trace.setPen(cyan)
spectrum4 = display(4)
spectrum4.trace.setPen(white)

###############################################################################
# GUI settings

# pyqtgraph settings for spectrum display
ui.graphWidget.setYRange(-110, 5)
ui.graphWidget.setXRange(88, 100)
ui.graphWidget.setBackground('k')  # black
ui.graphWidget.showGrid(x=True, y=True)
ui.graphWidget.addLine(y=6, movable=False, pen=red, label='', labelOpts={'position':0.05, 'color':('r')})
ui.graphWidget.addLine(y=0, movable=False, pen=red_dash, label='max', labelOpts={'position':0.025, 'color':('r')})
ui.graphWidget.addLine(y=-25, movable=False, pen=blue_dash, label='best', labelOpts={'position':0.025, 'color':('b')})
ui.graphWidget.setLabel('left', 'Signal', 'dBm')
ui.graphWidget.setLabel('bottom', 'Frequency MHz')
# spectrumDisplay = ui.graphWidget.plot([], [], name='Spectrum', pen=yellow, width=1)

# marker label positions
spectrum1.vline.label.setPosition(0.99)
spectrum2.vline.label.setPosition(0.96)
spectrum3.vline.label.setPosition(0.93)
spectrum4.vline.label.setPosition(0.90)

spectrum1.hline.label.setPosition(0.06)
spectrum2.hline.label.setPosition(1.0)
spectrum3.hline.label.setPosition(0.06)
spectrum4.hline.label.setPosition(1.0)


# pyqtgraph settings for time spectrum
axes = pyqtgl.GLAxisItem()
axes.setSize(450, 450, 120)  # x=blue, time.  y=yellow, freqs, z=green dBm
ui.openGLWidget.addItem(axes)

## Add a grid to the view
# g = pyqtgl.GLGridItem()
# g.scale(2,2,1)
# g.setDepthValue(10)  # draw grid after surfaces since they may be translucent
# ui.openGLWidget.addItem(g)

# voltage = tinySA.battery()
# ui.battery.setValue(voltage)



###############################################################################
# Connect signals from buttons and sliders

ui.scan_button.clicked.connect(scan)
ui.rbw_box.currentTextChanged.connect(rbw_changed)
ui.atten_box.valueChanged.connect(attenuate_changed)
ui.start_freq.editingFinished.connect(start_freq_changed)
ui.stop_freq.editingFinished.connect(stop_freq_changed)
ui.spur_button.clicked.connect(spur)
ui.lna_button.clicked.connect(lna)
ui.band_box.currentTextChanged.connect(band_changed)

# spectrum1.vline.sigPositionChanged.connect(spectrum1.setDiscrete)
spectrum1.vline.sigPositionChanged.connect(mkr1_moved)
spectrum2.vline.sigPositionChanged.connect(spectrum2.setDiscrete)
spectrum3.vline.sigPositionChanged.connect(spectrum3.setDiscrete)
spectrum4.vline.sigPositionChanged.connect(spectrum4.setDiscrete)

ui.marker1.stateChanged.connect(lambda: spectrum1.enableMarker(ui.marker1))
ui.marker2.stateChanged.connect(lambda: spectrum2.enableMarker(ui.marker2))
ui.marker3.stateChanged.connect(lambda: spectrum3.enableMarker(ui.marker3))
ui.marker4.stateChanged.connect(lambda: spectrum4.enableMarker(ui.marker4))
ui.mkr_start.clicked.connect(mStart)
ui.m2_type.currentTextChanged.connect(lambda: spectrum2.mType(ui.m2_type))
ui.m3_type.currentTextChanged.connect(lambda: spectrum3.mType(ui.m3_type))
ui.m4_type.currentTextChanged.connect(lambda: spectrum4.mType(ui.m4_type))

ui.t1_type.currentTextChanged.connect(lambda: spectrum1.tType(ui.t1_type))
ui.t2_type.currentTextChanged.connect(lambda: spectrum2.tType(ui.t2_type))
ui.t3_type.currentTextChanged.connect(lambda: spectrum3.tType(ui.t3_type))
ui.t4_type.currentTextChanged.connect(lambda: spectrum4.tType(ui.t4_type))

###############################################################################
# set up the application

ui.rbw_box.addItems(['auto', '0.2', '1', '3', '10', '30', '100', '300', '600', '850'])
ui.vbw_box.addItems(['auto'])
ui.points_box.addItems(['25', '50', '100', '200', '290', '450', '900', '1800', '3600', '7200', '15400'])
ui.points_box.setCurrentIndex(4)
ui.band_box.addItems(bands)
ui.t1_type.addItems(['Normal', 'Average', 'Max', 'Min'])
ui.t2_type.addItems(['Normal', 'Average', 'Max', 'Min'])
ui.t3_type.addItems(['Normal', 'Average', 'Max', 'Min'])
ui.t4_type.addItems(['Normal', 'Average', 'Max', 'Min'])
ui.m2_type.addItems(['Normal', 'Delta', 'Peak'])
ui.m3_type.addItems(['Normal', 'Delta', 'Peak'])
ui.m4_type.addItems(['Normal', 'Delta', 'Peak'])

tinySA.initialise()

window.show()

###############################################################################
# run the application until the user closes it

try:
    app.exec()
finally:
    exit_handler()  # close cleanly

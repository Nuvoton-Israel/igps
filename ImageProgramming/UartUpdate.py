# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os

uartUpdateTool = "Uartupdatetool"
linux_prefix = "sudo ./"

serialportnum_file = os.path.join(".", "SerialPortNumber.txt")
serialportbaudrate_file = os.path.join(".", "SerialPortBaudRate.txt")

global_serialPortNum = ""
global_serialBaudrate = 0

default_serialPortNum = "COM1"
default_serialBaudrate = 115200	

class UartError(Exception):
	def __init__(self, value):
		self.strerror = "UartUpdateTool error value:" + str(value)
	def __str__(self):
		return repr(self.strerror)

def uart_write_to_mem(port, baudrate, addr, file):

	_uartUpdateTool = uartUpdateTool
	if os.name != "nt":
		_uartUpdateTool = linux_prefix + uartUpdateTool

	cmd = "%s -port %s -baudrate %d -opr wr -addr %s -file %s" \
			% (_uartUpdateTool, port, baudrate, addr, file)
	rc = os.system(cmd)
	if rc != 0:
		expStr = "Writing %s to %s failed (port %s baudrate %d)" \
			% (file, addr, port, baudrate)
		raise UartError(expStr)

def uart_read_from_mem(port, baudrate, addr, size, file):

	_uartUpdateTool = uartUpdateTool
	if os.name != "nt":
		_uartUpdateTool = linux_prefix + uartUpdateTool

	cmd = "%s -port %s -baudrate %d -opr rd -addr %s -size %d -file %s" \
			% (_uartUpdateTool, port, baudrate, addr, size, file)
	rc = os.system(cmd)
	if rc != 0:
		expStr = "Reading from %s failed (port %s baudrate %d)" \
			% (addr, port, baudrate)
		raise UartError(expStr)

def uart_execute_nonreturn_code(port, baudrate, addr):

	_uartUpdateTool = uartUpdateTool
	if os.name != "nt":
		_uartUpdateTool = linux_prefix + uartUpdateTool

	cmd = "%s -port %s -baudrate %d -opr go -addr %s" \
			% (_uartUpdateTool, port, baudrate, addr)
	rc = os.system(cmd)
	if rc != 0:
		expStr = "Executing nonreturn code from %d failed (port %s baudrate %d)" \
			% (addr, port, baudrate)
		raise UartError(expStr)

def uart_execute_returnable_code(port, baudrate, addr):

	_uartUpdateTool = uartUpdateTool
	if os.name != "nt":
		_uartUpdateTool = linux_prefix + uartUpdateTool

	cmd = "%s -port %s -baudrate %d -opr call -addr %s" \
			% (_uartUpdateTool, port, baudrate, addr)
	rc = os.system(cmd)
	if rc != 0:
		expStr = "Executing returnable code from %d failed (port %s baudrate %d)" \
			% (addr, port, baudrate)
		raise UartError(expStr)

def updateSerialconigurationFiles(port, baudrate):

	file = open(serialportnum_file, "w")
	file.write("%s" % port)
	file.close()

	file = open(serialportbaudrate_file, "w")
	file.write("%s" % baudrate)
	file.close()

def check_com():

	global global_serialPortNum
	global global_serialBaudrate

	if global_serialPortNum != "" and global_serialBaudrate != 0:
		return [str(global_serialPortNum), int(global_serialBaudrate)]

	if os.path.isfile(serialportbaudrate_file):
		file = open(serialportbaudrate_file, "r")
		baudrate = int(file.read())
		file.close()
	else:
		print("Can't find baudrate configuration (%s), using %d") % (serialportbaudrate_file, default_serialBaudrate)
		baudrate = default_serialBaudrate

	print("----------------------------------------------------")
	print(" Scan COM ports, searching for a Poleg in UFPP mode ")
	print("----------------------------------------------------")
	_uartUpdateTool = uartUpdateTool
	if os.name != "nt":
		_uartUpdateTool = linux_prefix + uartUpdateTool

	cmd = "%s -opr scan -baudrate %d" % (_uartUpdateTool, baudrate)
	try:
		rc = os.system(cmd)
		if rc != 0:
			raise Exception
	except Exception as e:
		# try default baudrate
		cmd = "%s -opr scan -baudrate %d" % (_uartUpdateTool, default_serialBaudrate)
		rc = os.system(cmd)
		if rc != 0:
			print("Scanning failed. Port will be loaded from %s" % (serialportnum_file))
			raise e

		#default baudrate works
		baudrate = default_serialBaudrate

	if os.path.isfile(serialportnum_file):
		file = open(serialportnum_file, "r")
		port = file.read()
		file.close()
	else:
		print("Can't find serial port configuration (%s), using %d") % (serialportnum_file, default_serialPortNum)
		port = default_serialPortNum

	print("Serial Port settings:  %s; %s bps") % (port, baudrate)
	print("---------------------------------------------")
	
	global_serialPortNum = port
	global_serialBaudrate = baudrate
	
	updateSerialconigurationFiles(port, baudrate)
	
	return [str(port), int(baudrate)]

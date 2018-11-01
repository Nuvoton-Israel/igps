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

class UartError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def uart_write_to_mem(port, baudrate, addr, file):

	_uartUpdateTool = uartUpdateTool
	if os.name != "nt":
		_uartUpdateTool = linux_prefix + uartUpdateTool

	cmd = "%s -port %s -baudrate %d -opr wr -addr %s -file %s" \
			% (_uartUpdateTool, port, baudrate, addr, file)
	print(cmd)
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
	print(cmd)
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
	print(cmd)
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
	print(cmd)
	rc = os.system(cmd)
	if rc != 0:
		expStr = "Executing returnable code from %d failed (port %s baudrate %d)" \
			% (addr, port, baudrate)
		raise UartError(expStr)

def check_com():

	# initial values
	port = "COM1"
	baudrate = 115200
	
	print("----------------------------------------------------")
	print(" Scan COM ports, searching for a Poleg in UFPP mode ")
	print("----------------------------------------------------")
	
	_uartUpdateTool = uartUpdateTool
	if os.name != "nt":
		_uartUpdateTool = "./" + uartUpdateTool

	cmd = "%s -baudrate %d -opr scan" \
			% (_uartUpdateTool, baudrate)
	print(cmd)
	rc = os.system(cmd)

	if os.path.isfile(serialportnum_file):
		file = open(serialportnum_file, "r")
		port = file.read()
		file.close()

	if os.path.isfile(serialportbaudrate_file):
		file = open(serialportbaudrate_file, "r")
		baudrate = file.read()
		file.close()

	print("Serial Port settings:  %s; %s bps") % (port, baudrate)
	print("---------------------------------------------")
	print("")
	
	return [str(port), int(baudrate)]

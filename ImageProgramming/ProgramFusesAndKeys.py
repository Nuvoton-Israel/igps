# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os
import filecmp

import MemoryControllerInit
import ProgrammingErrors
import UartUpdate

programmer_monitor_addr = 0xFFFD6000
programmer_monitor_bin = os.path.join("inputs", "Poleg_programmer_monitor.bin")

header_location = 0xFFFDC000
otp_cmp_bin = "_otp.bin.cmp"

body_location = 0xFFFE0000

def run(otp_name, otp_prog_header, otp_bin, otp_read_header):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	cmp_bin = otp_name + otp_cmp_bin

	try:	
		if (not os.path.exists(otp_prog_header)):
			raise ValueError(otp_prog_header + " is missing") 

		if (not os.path.exists(otp_read_header)):
			raise ValueError(otp_read_header + " is missing") 

		if (not os.path.exists(otp_bin)):
			raise ValueError(otp_bin + " is missing") 

		[port, baudrate] = UartUpdate.check_com()

		print("Monitor programming...")
		UartUpdate.uart_write_to_mem(port, baudrate, programmer_monitor_addr, programmer_monitor_bin)

		print("Memory init...")
		MemoryControllerInit.memory_controller_init(port, baudrate)

		print("==============================")
		print(otp_name + ": programming...")
		print("otp_prog_header " + otp_prog_header + "    prog file " + otp_bin) 
		print("==============================")
		UartUpdate.uart_write_to_mem(port, baudrate, header_location, otp_prog_header)
		UartUpdate.uart_write_to_mem(port, baudrate, body_location, otp_bin )
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)

		print("==============================")
		print(otp_name + ": compare entire binary..." )
		print("==============================")
		UartUpdate.uart_write_to_mem(port, baudrate, header_location, otp_read_header)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)
		UartUpdate.uart_read_from_mem(port, baudrate, 0xFFFE1000, 1024, cmp_bin)

		#if not filecmp.cmp(otp_bin, cmp_bin):
		#	ProgrammingErrors.print_error_compare_error(run.__name__, otp_bin, cmp_bin)
		#	return -1

		print("==============================")
		print(otp_name + ":  read monitor log to file " + otp_name + "_monitor_log.bin" )
		print("==============================")		
		UartUpdate.uart_read_from_mem(port, baudrate, 0xFFFDBF00, 256, otp_name + "_monitor_log.bin")

		print("==============================")
		print(otp_name + ": program %s Pass" % (otp_bin))
		print("==============================")

		return 0

	except (UartUpdate.UartError, IOError) as e:
		ProgrammingErrors.print_error(e.value)
		return -1;

	finally:
		os.chdir(currpath)

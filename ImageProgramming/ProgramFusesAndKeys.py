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

FW_header_location = 0xFFFDC000
FW_and_Header_cmp = "FW_and_Header.cmp"


def run(FW_body_location, FW_and_Header_bin, FW_Programming_bin):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		print("Monitor programming...")
		UartUpdate.uart_write_to_mem(port, baudrate, programmer_monitor_addr, programmer_monitor_bin)

		print("Memory init...")
		MemoryControllerInit.memory_controller_init(port, baudrate)

		print("==============================")
		print("Programming...")
		print("==============================")
		UartUpdate.uart_write_to_mem(port, baudrate, FW_header_location, FW_Programming_bin)
		UartUpdate.uart_write_to_mem(port, baudrate, FW_body_location, FW_and_Header_bin)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)

		print("==============================")
		print("Compare entire binary...")
		print("==============================")
		UartUpdate.uart_write_to_mem(port, baudrate, FW_header_location, FW_Read_bin)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)
		UartUpdate.uart_read_from_mem(port, baudrate, 0xFFFE1000, 1024, FW_and_Header_cmp)
		
		if not filecmp.cmp(FW_and_Header_bin, FW_and_Header_cmp):
			print_error_compare_error(func_name, FW_and_Header_bin, FW_and_Header_cmp)
			return -1

		print("==============================")
		print("Program %s Pass" % (FW_and_Header_bin))
		print("==============================")

		return 0

	except (UartUpdate.UartError, IOError) as e:
		ProgrammingErrors.print_error(e.value)
		return -1;

	finally:
		os.chdir(currpath)

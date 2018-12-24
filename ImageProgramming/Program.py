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
	
		print("Calculate size...")
		FW_bin_size = os.path.getsize(FW_and_Header_bin)
		print("%s size = %d") % (FW_and_Header_bin, FW_bin_size)

		print("Monitor programming...")
		UartUpdate.uart_write_to_mem(port, baudrate, programmer_monitor_addr, programmer_monitor_bin)

		print("Memory init...")
		MemoryControllerInit.memory_controller_init(port, baudrate)

		print("==============================")
		print("  read monitor log to file MC_init_flash_prog_monitor_log.bin" )
		print("==============================")		
		UartUpdate.uart_read_from_mem(port, baudrate, 0xFFFDBF00, 256, "MC_init_flash_prog_monitor_log.bin")
		print("==============================")
		print("Programming...")
		print("==============================")
		UartUpdate.uart_write_to_mem(port, baudrate, FW_header_location, FW_Programming_bin)
		UartUpdate.uart_write_to_mem(port, baudrate, FW_body_location, FW_and_Header_bin)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)
		print("==============================")
		print("  read monitor log to file Prog_flash_prog_monitor_log.bin" )
		print("==============================")		
		UartUpdate.uart_read_from_mem(port, baudrate, 0xFFFDBF00, 256, "Prog_flash_prog_monitor_log.bin")

		print("==============================")
		print("Compare entire binary...")
		print("==============================")
		UartUpdate.uart_read_from_mem(port, baudrate, 0x80000000, FW_bin_size, FW_and_Header_cmp)
		
		print("==============================")
		print("  read monitor log to file cmp_flash_prog_monitor_log.bin" )
		print("==============================")		
		UartUpdate.uart_read_from_mem(port, baudrate, 0xFFFDBF00, 256, "cmp_flash_prog_monitor_log.bin")
		
		
		
		
		if not filecmp.cmp(FW_and_Header_bin, FW_and_Header_cmp):
			print("Comparison Failed! (%s vs %s)" % (FW_and_Header_bin, FW_and_Header_cmp))
			raise IOError

		print("==============================")
		print("Program %s Pass" % (FW_and_Header_bin))
		print("==============================")

	except (UartUpdate.UartError, IOError) as e:
		print("==============================")
		print("  read monitor log to file flash_prog_monitor_log.bin" )
		print("==============================")		
		UartUpdate.uart_read_from_mem(port, baudrate, 0xFFFDBF00, 256, "flash_prog_monitor_log.bin")

		print(e.strerror)
		raise

	finally:
		os.chdir(currpath)

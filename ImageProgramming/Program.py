# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2019 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os
import filecmp
import struct

import ProgrammerMonitor


FW_and_Header_cmp = "FW_and_Header.cmp"


def run(FW_and_Header_bin, FW_Programming_bin):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		print("Calculate size...")
		FW_bin_size = os.path.getsize(FW_and_Header_bin)
		print("%s size = %d") % (FW_and_Header_bin, FW_bin_size)

		ProgrammerMonitor.load_monitor()

		print("==============================")
		print("Programming...")
		print("==============================")
		ProgrammerMonitor.spi_program_from_sRam(FW_Programming_bin, FW_and_Header_bin)
		ProgrammerMonitor.read_monitor_log("Prog_flash_prog_monitor_log.bin")

		print("==============================")
		print("Compare binary...")
		print("==============================")
		ProgrammerMonitor.spi_read(FW_bin_size, FW_and_Header_cmp)
		ProgrammerMonitor.read_monitor_log("cmp_flash_prog_monitor_log.bin")
		if not filecmp.cmp(FW_and_Header_bin, FW_and_Header_cmp):
			print("Comparison Failed! (%s vs %s)" % (FW_and_Header_bin, FW_and_Header_cmp))
			raise IOError

		print("==============================")
		print("Program %s Passed" % (FW_and_Header_bin))
		print("==============================")

	except Exception as e:
		print("Program %s Failed" % FW_and_Header_bin)
		ProgrammerMonitor.read_monitor_log("flash_prog_monitor_log.bin")
		raise

	finally:
		os.chdir(currpath)

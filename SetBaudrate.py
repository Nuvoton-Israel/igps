# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import os
import sys
import struct

import ImageProgramming.ProgrammerMonitor

try:
	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	if len(sys.argv) < 2:
		baudrate = 750000

	if len(sys.argv) == 2:
		try:
			baudrate = int(sys.argv[1])
		except Exception:
			print ("Invalid Parameter")
			raise

	if len(sys.argv) > 2:
		raise Exception("Too many arguments")

	ImageProgramming.ProgrammerMonitor.load_monitor()
	ImageProgramming.ProgrammerMonitor.set_baudrate(baudrate)

except Exception as e:
	print(e)
finally:
	os.chdir(currpath)
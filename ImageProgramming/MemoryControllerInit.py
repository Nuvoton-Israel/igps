# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------


import sys
import os

import UartUpdate

header_location = 0xFFFDC000
programmer_monitor_addr = 0xFFFD6000
MC_InitHeader = os.path.join("inputs", "MC_INIT_TAG.bin")

def memory_controller_init(port, baudrate):

	try:
		UartUpdate.uart_write_to_mem(port, baudrate, header_location, MC_InitHeader)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)

		print("MC Init Passed")

	except Exception as e:
		print("MC Init Failed")
		raise

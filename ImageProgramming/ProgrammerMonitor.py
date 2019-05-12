# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2019 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------


import sys
import os
import struct

import UartUpdate

MC_INIT_TAG = 0xA50750A9
MC_InitHeader = os.path.join("inputs", "MC_Init.bin")

UART_SETTING_TAG = 0xA50750A8
UART_SettingHeader = os.path.join("inputs", "UART_Setting.bin")

HEADER_address = 0xFFFDC000
HEADER_bin_size_offset = 0x04
HEADER_spi_addr_offset = 0x08
HEADER_ram_addr_offset = 0x1c

programmer_monitor_addr = 0xFFFD6000
programmer_monitor_log_addr = 0xFFFDBF00
programmer_monitor_log_size = 0x100
programmer_monitor_bin = os.path.join("inputs", "Poleg_programmer_monitor.bin")

SRAM_address = 0xFFFE0000
DDR_address  = 0x100000

SRAM_size = (64 * 1024)

SPI_adrerss = 0x80000000

def create_header(tag, filename):

	_file = open(filename, "wb")
	_file.write(struct.pack('I', tag))
	_file.close()


def load_monitor():

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		print("Loading monitor...")
		UartUpdate.uart_write_to_mem(port, baudrate, programmer_monitor_addr, programmer_monitor_bin)

		print("Monitor Loading Passed")

	except Exception as e:
		print("Monitor Loading Failed")
		raise

	finally:
		os.chdir(currpath)


def read_monitor_log(logfile):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		print("==============================")
		print("  read monitor log to %s" % logfile)
		print("==============================")
		UartUpdate.uart_read_from_mem(port, baudrate, programmer_monitor_log_addr, programmer_monitor_log_size, logfile)

		print("Loading Monitor Log Passed")

	except Exception as e:
		print("Loading Monitor Log Failed")
		raise

	finally:
		os.chdir(currpath)


def memory_controller_init(port, baudrate):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		create_header(MC_INIT_TAG, MC_InitHeader)
		UartUpdate.uart_write_to_mem(port, baudrate, HEADER_address, MC_InitHeader)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)

		print("MC Init Passed")

	except Exception as e:
		print("MC Init Failed")
		raise

	finally:
		os.chdir(currpath)


def spi_program_from_sRam(header_file, image_file):

	chunk_header_file = "sram_chunk_64k_header.bin"
	chunk_file = "sram_chunk_64k.bin"

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		_file = open(header_file, "rb")
		header = bytearray(_file.read())
		_file.close()

		_file = open(image_file, "rb")
		image = bytearray(_file.read())
		_file.close()

		image_size = len(image)

		for offset in range(0, image_size, SRAM_size):

			print("******************************")
			print("***** Programming... %d/%d *****") % (offset / SRAM_size, image_size / SRAM_size)
			print("******************************")

			chunk = image[offset : (offset + SRAM_size)]

			header[HEADER_bin_size_offset:HEADER_bin_size_offset + 4] = struct.pack('I', len(chunk))
			header[HEADER_spi_addr_offset:HEADER_spi_addr_offset + 4] = struct.pack('I', SPI_adrerss + offset)
			header[HEADER_ram_addr_offset:HEADER_ram_addr_offset + 4] = struct.pack('I', SRAM_address)
		
			file = open(chunk_header_file, "wb")
			file.write(header)
			file.close()
		
			file = open(chunk_file, "wb")
			file.write(chunk)
			file.close()

			UartUpdate.uart_write_to_mem(port, baudrate, HEADER_address, chunk_header_file)
			UartUpdate.uart_write_to_mem(port, baudrate, SRAM_address, chunk_file)
			UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)
	
		print("SPI Programming Passed")

	except Exception as e:
		print("SPI Programming Failed")
		raise

	finally:
		os.chdir(currpath)


def spi_program_from_ddr(header_file, image_file):

	header_filename = "ddr_image_header.bin"

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		print("DDR init...")
		memory_controller_init(port, baudrate)

		_file = open(header_file, "rb")
		header = bytearray(_file.read())
		_file.close()

		_file = open(image_file, "rb")
		image = bytearray(_file.read())
		_file.close()

		header[HEADER_ram_addr_offset:HEADER_ram_addr_offset + 4] = struct.pack('I', DDR_address)

		file = open(header_file, "wb")
		file.write(header)
		file.close()

		print("==============================")
		print("Programming...")
		print("==============================")
		UartUpdate.uart_write_to_mem(port, baudrate, HEADER_address, header_file)
		UartUpdate.uart_write_to_mem(port, baudrate, DDR_address, image_file)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)
		
		print("SPI Programming Passed")

	except Exception as e:
		print("SPI Programming Failed")
		raise

	finally:
		os.chdir(currpath)


def spi_read(size, file):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		print("==============================")
		print("Reading 0x%x bytes from SPI..." % size)
		print("==============================")
		UartUpdate.uart_read_from_mem(port, baudrate, SPI_adrerss, size, file)
		
		print("==============================")
		print("  Read monitor log to file cmp_flash_prog_monitor_log.bin" )
		print("==============================")		
		UartUpdate.uart_read_from_mem(port, baudrate, programmer_monitor_log_addr, programmer_monitor_log_size, "cmp_flash_prog_monitor_log.bin")

		print("SPI Reading Passed")

	except Exception as e:
		print("SPI Reading Failed")
		raise

	finally:
		os.chdir(currpath)


def fuse_program(otp_name, header_file, image_file):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		UartUpdate.uart_write_to_mem(port, baudrate, HEADER_address, header_file)
		UartUpdate.uart_write_to_mem(port, baudrate, SRAM_address, image_file)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)
		
		print("%s Programming Passed" % otp_name)

	except Exception as e:
		print("%s Programming Failed" % otp_name)
		raise

	finally:
		os.chdir(currpath)


def fuse_read(otp_name, size, header_file, image_file):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		UartUpdate.uart_write_to_mem(port, baudrate, HEADER_address, header_file)
		UartUpdate.uart_execute_returnable_code(port, baudrate, programmer_monitor_addr)
		UartUpdate.uart_read_from_mem(port, baudrate, SRAM_address + 0x1000, size, image_file)

		print("%s Reading Passed" % otp_name)	

	except Exception as e:
		print("%s Reading Failed" % otp_name)
		raise

	finally:
		os.chdir(currpath)


def set_baudrate(baudrate_to_set):

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		[port, baudrate] = UartUpdate.check_com()

		create_header(UART_SETTING_TAG, UART_SettingHeader)
		_file = open(UART_SettingHeader, "ab")
		_file.write(struct.pack('I', baudrate_to_set))
		_file.close()

		print("Monitor programming...")
		UartUpdate.uart_write_to_mem(port, baudrate, programmer_monitor_addr, programmer_monitor_bin)

		print("==============================")
		print("Header writing...")
		print("==============================")
		UartUpdate.uart_write_to_mem(port, baudrate, HEADER_address, UART_SettingHeader)
		UartUpdate.uart_execute_nonreturn_code(port, baudrate, programmer_monitor_addr)

		file = open(UartUpdate.serialportbaudrate_file, "w")
		file.write("%s" % baudrate_to_set)
		file.close()

		print("Baudrate Setting Passed (set to %d)" % baudrate_to_set)

	except Exception as e:
		print("Baudrate Setting Failed")
		raise

	finally:
		os.chdir(currpath)

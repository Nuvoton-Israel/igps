# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2019 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os
import filecmp

import ProgrammingErrors
import ProgrammerMonitor

otp_cmp_bin = "_otp.bin.cmp"

otp_size = 1024

def not_8(x): return (x ^ 0xff)
def is_valid_write(curr, to_program): return (not_8(curr) | (curr & to_program)) == 0xff

def nibble_parity_check(fuse_array, otp, field):

	offset = otp[field][0]
	size = otp[field][1] - otp[field][0]

	# for each byte in the field
	for i in range(0, size * 2):

		E0 = (fuse_array[offset + i] >> 0) & 0x01
		E1 = (fuse_array[offset + i] >> 1) & 0x01
		E2 = (fuse_array[offset + i] >> 2) & 0x01
		E3 = (fuse_array[offset + i] >> 3) & 0x01

		dataout = fuse_array[offset + i] & 0x0f
		dataout |= (E0 ^ E1) << 4
		dataout |= (E2 ^ E3) << 5
		dataout |= (E0 ^ E2) << 6
		dataout |= (E1 ^ E3) << 7

		if dataout != fuse_array[offset + i]:
			raise Exception("Nibble parity error in field %s, image cannot be programmed" % field)

	return fuse_array


# check if there are 0's that are going to be written on '1's
def majority_check(fuse_array, otp, field):

	offset = otp[field][0]
	size = otp[field][1] - otp[field][0]

	# for each byte in the field
	for i in range(0, size):
		if fuse_array[offset + i] != fuse_array[offset + size + i] or fuse_array[offset + i] != fuse_array[offset + size * 2 + i]:
			raise Exception("Majority error in field %s, image cannot be programmed" % field)

	return fuse_array


# check if there are 0's that are going to be written on '1's
def valididity_check(current_fuse_array, fuse_array_to_program, otp, field):

	curr = current_fuse_array[otp[field][0]:otp[field][1]]
	to_prog = fuse_array_to_program[otp[field][0]:otp[field][1]]
	field_size = otp[field][1] - otp[field][0]

	# for each byte in the field
	for i in range(0, field_size):
		if not is_valid_write(curr[i], to_prog[i]):
			# Show warning if any '0' bit is going to be programmed on '1' bit, and change it to '1'
			fuse_array_to_program[otp[field][0] + i] |= curr[i]
			print("byte %d in %s (=0x%x) cannot be programmed to the otp (current value is 0x%x)" % (i, field, to_prog[i], curr[i]))

	return fuse_array_to_program


fuse_fields = {
	'FUSTRAP': (0, 4, majority_check),
	'CP_FUSTRAP': (12, 14, majority_check),
	'DAC_Calibration_Word': (16, 20, nibble_parity_check),
	'ADC_Calibration_Word': (24, 28, nibble_parity_check),
	'Verification_Fault_Module_Protection': (32, 36, nibble_parity_check),
	'oFSVFP': (40, 42, majority_check),
	'oFSAP': (52, 54, majority_check),
	'oKAP': (58, 60, majority_check),
	'Derivative_Word': (64, 68, nibble_parity_check),
	'oPKValue2_second_half': (256, 384, nibble_parity_check),
	'oPKValue1': (512, 768, nibble_parity_check)
}

key_fields = {
	'oAESKEY0': (0, 32, nibble_parity_check),
	'oAESKEY1': (64, 96, nibble_parity_check),
	'oAESKEY2': (128, 160, nibble_parity_check),
	'oAESKEY3': (192, 224, nibble_parity_check),
	'oPKValue2_first_half': (256, 384, nibble_parity_check),
	'oPKValue0': (512, 768, nibble_parity_check)
}


def check_fields(current_fuse_array, fuse_array_to_program, otp):

	# check fields, change the fuse array if needed
	for field in otp:
		fuse_array_to_program = otp[field][2](fuse_array_to_program, otp, field)
		fuse_array_to_program = valididity_check(current_fuse_array, fuse_array_to_program, otp, field)

	return fuse_array_to_program


def check_otp_bin(otp_name, current_otp_filename, otp_bin_filename):

	_file = open(current_otp_filename, "rb")
	current = bytearray(_file.read())
	_file.close()

	_file = open(otp_bin_filename, "rb")
	to_program = bytearray(_file.read())
	_file.close()

	origin_to_program = to_program[:]

	if otp_name == "fuse":
		to_program = check_fields(current, to_program, fuse_fields)
	elif otp_name == "key":
		to_program = check_fields(current, to_program, key_fields)
	else:
		raise Exception("Error: '%s' is otp name is not valid" % otp_name)

	# check if the fuse array was changed
	if cmp(origin_to_program, to_program) != 0:

		reply = str(raw_input("Warning: otp is not empty, after programming the otp may be different from the input image. Type 'y' to continue:").strip())
		if reply != "y":
			raise Exception("OTP image cannot be programmed, please modify your otp map file")

		modified_otp_bin_filename = "%s.modified" % otp_bin_filename
		_file = open(modified_otp_bin_filename, "wb")
		_file.write(to_program)
		_file.close()

		return modified_otp_bin_filename

	return otp_bin_filename


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

		ProgrammerMonitor.load_monitor()

		print("==============================")
		print(otp_name + ": read otp..." )
		print("==============================")
		ProgrammerMonitor.fuse_read(otp_name, otp_size, otp_read_header, cmp_bin)

		# check if the input file can be programmed to the otp
		otp_bin = check_otp_bin(otp_name, cmp_bin, otp_bin)

		print("==============================")
		print(otp_name + ": programming...")
		print("otp_prog_header " + otp_prog_header + "    prog file " + otp_bin) 
		print("==============================")
		ProgrammerMonitor.fuse_program(otp_name, otp_prog_header, otp_bin)
		
		print("==============================")
		print(otp_name + ": compare entire binary..." )
		print("==============================")
		ProgrammerMonitor.fuse_read(otp_name, otp_size, otp_read_header, cmp_bin)
		if not filecmp.cmp(otp_bin, cmp_bin):
			ProgrammingErrors.print_error_compare_error(run.__name__, otp_bin, cmp_bin)

		ProgrammerMonitor.read_monitor_log(otp_name + "_monitor_log.bin")

		print("==============================")
		print(otp_name + ": program %s Pass" % (otp_bin))
		print("==============================")

	except Exception as e:
		print("Program %s Failed" % otp_bin)
		ProgrammerMonitor.read_monitor_log("otp_prog_monitor_log.bin")
		raise

	finally:
		os.chdir(currpath)

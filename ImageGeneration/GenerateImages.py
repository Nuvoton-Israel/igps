# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os

from shutil import copy
from shutil import move
from shutil import rmtree

from BinaryGenerator import *
from BinarySignatureGenerator import *

inputs_dir = "inputs"
outputs_dir = "output_binaries"

basic_outputs_dir = os.path.join(outputs_dir, "Basic")
secure_outputs_dir = os.path.join(outputs_dir, "Secure")

BootBlockAndHeader_xml = os.path.join(inputs_dir, "BootBlockAndHeader.xml")
BootBlockAndHeader_bin = os.path.join(outputs_dir, "BootBlockAndHeader.bin")
BootBlockAndHeader_basic_bin = os.path.join(basic_outputs_dir, "BootBlockAndHeader.bin")
BootBlockAndHeader_secure_bin = os.path.join(secure_outputs_dir, "BootBlockAndHeader.bin")

UbootAndHeader_xml = os.path.join(inputs_dir, "UbootHeader.xml")
UbootAndHeader_bin = os.path.join(outputs_dir, "UbootAndHeader.bin")
UbootAndHeader_basic_bin = os.path.join(basic_outputs_dir, "UbootAndHeader.bin")
UbootAndHeader_secure_bin = os.path.join(secure_outputs_dir, "UbootAndHeader.bin")

mergedBootBlockAndUboot_xml = os.path.join(inputs_dir, "mergedBootBlockAndUboot.xml")
mergedBootBlockAndUboot_basic_bin = os.path.join(basic_outputs_dir, "mergedBootBlockAndUboot.bin")
mergedBootBlockAndUboot_secure_bin = os.path.join(secure_outputs_dir, "mergedBootBlockAndUboot.bin")

merged_1FF_xml = os.path.join(inputs_dir, "merged_1FF.xml")
merged_1FF_basic_bin = os.path.join(basic_outputs_dir, "merged_1FF.bin")

rsa_private_key_0_bin = os.path.join(inputs_dir, "rsa_private_key_0.bin")
rsa_public_key_0_bin = os.path.join(inputs_dir, "rsa_public_key_0.bin")

poleg_key_map_xml = os.path.join(inputs_dir, "poleg_key_map.xml")
poleg_key_map_bin = os.path.join(secure_outputs_dir, "poleg_key_map.bin")

poleg_fuse_map_xml = os.path.join(inputs_dir, "poleg_fuse_map.xml")
poleg_fuse_map_bin = os.path.join(secure_outputs_dir, "poleg_fuse_map.bin")


def run():

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		if os.path.isdir(outputs_dir):
			rmtree(outputs_dir)
		os.mkdir(outputs_dir)

		if os.path.isdir(basic_outputs_dir):
			rmtree(basic_outputs_dir)
		os.mkdir(basic_outputs_dir)

		print("==========================================================")
		print("== Generating %s" % (BootBlockAndHeader_bin))
		generate_binary(BootBlockAndHeader_xml, BootBlockAndHeader_bin)

		print("==========================================================")
		print("== Generating %s" % (UbootAndHeader_bin))
		generate_binary(UbootAndHeader_xml, UbootAndHeader_bin)

		print("==========================================================")
		print("== Merging %s and %s" % (BootBlockAndHeader_bin, UbootAndHeader_bin))
		generate_binary(mergedBootBlockAndUboot_xml, mergedBootBlockAndUboot_basic_bin)

		try:
			print("==========================================================")
			print("== Merging %s and %s and linux" % (BootBlockAndHeader_bin, UbootAndHeader_bin))
			generate_binary(merged_1FF_xml, merged_1FF_basic_bin)
		except:
			print("Warning: Merged image of %s and %s and linux was not generated" % (BootBlockAndHeader_bin, UbootAndHeader_bin))

		print("")
		print("==========================================================")
		print("== Starting Signature prodedure")
		print("==========================================================")
		print("")

		if os.path.isdir(secure_outputs_dir):
			rmtree(secure_outputs_dir)
		os.mkdir(secure_outputs_dir)

		copy(BootBlockAndHeader_bin, BootBlockAndHeader_basic_bin)
		copy(UbootAndHeader_bin, UbootAndHeader_basic_bin)
		
		print("==========================================================")
		print("== Signing %s" % (BootBlockAndHeader_secure_bin))
		sign_binary(BootBlockAndHeader_bin, 0x140, rsa_private_key_0_bin, \
			rsa_public_key_0_bin, 0x8, BootBlockAndHeader_bin)

		print("==========================================================")
		print("== Signing %s" % (mergedBootBlockAndUboot_secure_bin))
		sign_binary(UbootAndHeader_bin, 0x140, rsa_private_key_0_bin, \
			rsa_public_key_0_bin, 0x8, UbootAndHeader_bin)

		print("==========================================================")
		print("== Merging %s and %s" % (BootBlockAndHeader_bin, UbootAndHeader_bin))
		generate_binary(mergedBootBlockAndUboot_xml, mergedBootBlockAndUboot_secure_bin)

		move(BootBlockAndHeader_bin, BootBlockAndHeader_secure_bin)
		move(UbootAndHeader_bin, UbootAndHeader_secure_bin)

		print("==========================================================")
		print("== Generating %s" % (poleg_key_map_bin))
		generate_binary(poleg_key_map_xml, poleg_key_map_bin)

		print("==========================================================")
		print("== Generating %s" % (poleg_fuse_map_bin))
		generate_binary(poleg_fuse_map_xml, poleg_fuse_map_bin)

	except (Exception) as e:
		print("Error building binaries (%s)" % (e.strerror))
		raise

	finally:
		os.chdir(currpath)

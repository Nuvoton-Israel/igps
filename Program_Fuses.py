# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2019 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import os

import ImageGeneration.BinaryGenerator
import ImageProgramming.ProgramOtp

Programming_inputs_dir = os.path.join("ImageProgramming", "inputs")
Intermediate_dir = os.path.join("ImageGeneration", "intermediate")

KEY_bin = os.path.join("ImageGeneration", "output_binaries", "Secure", "poleg_key_map.bin")

KEY_Programming_xml = os.path.join(Programming_inputs_dir, "keyProgrammingHeader.xml")
KEY_prog_header = os.path.join(Intermediate_dir, "KeyProgrammingHeader.bin")
KEY_Reading_xml = os.path.join(Programming_inputs_dir, "keyReadHeader.xml")
KEY_read_header = os.path.join(Intermediate_dir, "keyReadHeader.bin")

FUSE_bin = os.path.join("ImageGeneration", "output_binaries", "Secure", "poleg_fuse_map.bin")

FUSE_Programming_xml = os.path.join(Programming_inputs_dir, "fuseProgrammingHeader.xml")
FUSE_prog_header = os.path.join(Intermediate_dir, "FuseProgrammingHeader.bin")
FUSE_Reading_xml = os.path.join(Programming_inputs_dir, "fuseReadHeader.xml")
FUSE_read_header = os.path.join(Intermediate_dir, "fuseReadHeader.bin")

try:
	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	if not os.path.isdir(Intermediate_dir):
		os.mkdir(Intermediate_dir)
			
	################################################################
	# KEY Programming
	################################################################	

	ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(KEY_Programming_xml),	\
														os.path.abspath(KEY_prog_header))

	ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(KEY_Reading_xml),		\
														os.path.abspath(KEY_read_header))

	msg = "Are you sure you want to program keys (cannot be changed later)? (y/n)"
	reply = str(raw_input(msg).strip())
	if reply == "y":
		print("==============================")
		print("Program Keys...")
		print("==============================")
		ImageProgramming.ProgramOtp.run("key",  os.path.abspath(KEY_prog_header),	\
												os.path.abspath(KEY_bin),			\
												os.path.abspath(KEY_read_header))
	else:
		print("Key programming was skipped")

	################################################################
	# FUSE Programming
	################################################################
	ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(FUSE_Programming_xml),	\
														os.path.abspath(FUSE_prog_header))

	ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(FUSE_Reading_xml),		\
														os.path.abspath(FUSE_read_header))	

	msg = "Are you sure you want to program fuses (one time programming)? (y/n)"
	reply = str(raw_input(msg).strip())
	if reply == "y":
		print("==============================")
		print("Program Fuses...")
		print("==============================")
		ImageProgramming.ProgramOtp.run("fuse", os.path.abspath(FUSE_prog_header),	\
												os.path.abspath(FUSE_bin),			\
												os.path.abspath(FUSE_read_header))
	else:
		print("Fuse programming was skipped")

except Exception as e:
	print(str(e))
# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import os

import ImageGeneration.BinaryGenerator
import ImageProgramming.ProgramFusesAndKeys


FW_body_location = 0x100000

Programming_inputs_dir = os.path.join("ImageProgramming", "inputs")
Intermediate_dir = os.path.join("ImageGeneration", "intermediate")

KeyArray_bin = os.path.join("ImageGeneration", "output_binaries", "Secure", "poleg_key_map.bin")

KEY_Programming_xml = os.path.join(Programming_inputs_dir, "keyProgrammingHeader.xml")
KEY_Programming_bin = os.path.join(Intermediate_dir, "KeyProgrammingHeader.bin")
KEY_Reading_xml = os.path.join(Programming_inputs_dir, "keyReadHeader.xml")
KEY_Reading_bin = os.path.join(Intermediate_dir, "keyReadHeader.bin")

FuseArray_bin = os.path.join("ImageGeneration", "output_binaries", "Secure", "poleg_fuse_map.bin")

FUSE_Programming_xml = os.path.join(Programming_inputs_dir, "fuseProgrammingHeader.xml")
FUSE_Programming_bin = os.path.join(Intermediate_dir, "FuseProgrammingHeader.bin")
FUSE_Reading_xml = os.path.join(Programming_inputs_dir, "fuseReadHeader.xml")
FUSE_Reading_bin = os.path.join(Intermediate_dir, "fuseReadHeader.bin")

def run():

	try:
		if not os.path.isdir(Intermediate_dir):
			os.mkdir(Intermediate_dir)

		ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(KEY_Programming_xml),	\
															os.path.abspath(KEY_Programming_bin))

		ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(KEY_Reading_xml),		\
															os.path.abspath(KEY_Reading_bin))

		ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(FUSE_Programming_xml),	\
															os.path.abspath(FUSE_Programming_bin))

		ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(FUSE_Reading_xml),		\
															os.path.abspath(FUSE_Reading_bin))

		msg = "Are you sure you want to program keys (cannot be changed later)? (y/n)"
		reply = str(raw_input(msg).strip())
		if reply == "y":
			print("==============================")
			print("Program Keys...")
			print("==============================")
			#ImageProgramming.ProgramFusesAndKeys(	FW_body_location,			\
			#							os.path.abspath(KeyArray_bin),			\
			#							os.path.abspath(KEY_Programming_bin),	\
			#							os.path.abspath(KEY_Reading_bin))
		else:
			print("Key programming was skipped")

		msg = "Are you sure you want to program fuses (one time programming)? (y/n)"
		reply = str(raw_input(msg).strip())
		if reply == "y":
			print("==============================")
			print("Program Fuses...")
			print("==============================")
			#ImageProgramming.ProgramFusesAndKeys(	FW_body_location,			\
			#							os.path.abspath(FuseArray_bin),			\
			#							os.path.abspath(FUSE_Programming_bin),	\
			#							os.path.abspath(FUSE_Reading_bin))
		else:
			print("Fuse programming was skipped")

	except Exception as e:
		print(e)
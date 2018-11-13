# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import os

from shutil import copyfile

import ImageGeneration.BinaryGenerator
import ImageProgramming.Program

FW_body_location = 0xFFFE0000

Programming_inputs_dir = os.path.join("ImageProgramming", "inputs")
Intermediate_dir = os.path.join("ImageGeneration", "intermediate")

FW_and_Header_bin = os.path.join("ImageGeneration", "output_binaries", "Basic", "BootBlockAndHeader.bin")

FW_Programming_xml = os.path.join(Programming_inputs_dir, "BootBlockProgramming.xml")
FW_Programming_bin = os.path.join(Intermediate_dir, "BootBlockProgramming.bin")
FW_bin_intermediate = os.path.join(Intermediate_dir, "BootBlockAndHeader.bin")

try:
	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	if not os.path.isdir(Intermediate_dir):
		os.mkdir(Intermediate_dir)

	copyfile(FW_and_Header_bin, FW_bin_intermediate)

	ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(FW_Programming_xml),	\
														os.path.abspath(FW_Programming_bin))

	ImageProgramming.Program.run(	FW_body_location,						\
									os.path.abspath(FW_and_Header_bin),		\
									os.path.abspath(FW_Programming_bin))
except Exception as e:
	print(e)
finally:
	os.chdir(currpath)
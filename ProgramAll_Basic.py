# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2019 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import os

from shutil import copyfile

import ImageGeneration.BinaryGenerator
import ImageProgramming.Program

Programming_inputs_dir = os.path.join("ImageProgramming", "inputs")
Intermediate_dir = os.path.join("ImageGeneration", "intermediate")

FW_and_Header_bin = os.path.join("ImageGeneration", "output_binaries", "Basic", "mergedBootBlockAndUboot.bin")

FW_Programming_xml = os.path.join(Programming_inputs_dir, "MergedProgramming.xml")
FW_Programming_bin = os.path.join(Intermediate_dir, "MergedProgramming.bin")
FW_bin_intermediate = os.path.join(Intermediate_dir, "mergedBootBlockAndUboot.bin")

try:
	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	if not os.path.isdir(Intermediate_dir):
		os.mkdir(Intermediate_dir)

	copyfile(FW_and_Header_bin, FW_bin_intermediate)

	ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(FW_Programming_xml),	\
														os.path.abspath(FW_Programming_bin))

	ImageProgramming.Program.run(	os.path.abspath(FW_and_Header_bin),		\
									os.path.abspath(FW_Programming_bin))
except Exception as e:
	print(e)
finally:
	os.chdir(currpath)
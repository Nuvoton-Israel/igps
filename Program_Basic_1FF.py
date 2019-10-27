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

FW_and_Header_bin = os.path.join("ImageGeneration", "output_binaries", "Basic", "merged_1FF.bin")

FW_Programming_xml = os.path.join(Programming_inputs_dir, "MergedProgramming_1FF.xml")
FW_Programming_bin = os.path.join(Intermediate_dir, "MergedProgramming_1FF.bin")
FW_bin_intermediate = os.path.join(Intermediate_dir, "merged_1FF.bin")

try:
	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))
	print("Move to " + os.path.dirname(os.path.abspath(__file__)))

	if not os.path.isdir(Intermediate_dir):
		os.mkdir(Intermediate_dir)
		
	if not os.path.isfile(FW_and_Header_bin):
		print("missing: " + FW_and_Header_bin)
		
	if not os.path.isfile(FW_Programming_xml):
		print("missing: " + FW_Programming_xml)
		

	copyfile(FW_and_Header_bin, FW_bin_intermediate)

	ImageGeneration.BinaryGenerator.generate_binary(	os.path.abspath(FW_Programming_xml),	\
														os.path.abspath(FW_Programming_bin))
														
	if not os.path.isfile(FW_Programming_bin):
		print("missing: " + FW_Programming_bin)
		
	if not os.path.isfile(FW_bin_intermediate):
		print("missing: " + FW_bin_intermediate)

	ImageProgramming.Program.run(	os.path.abspath(FW_and_Header_bin),		\
									os.path.abspath(FW_Programming_bin))
except Exception as e:
	print(e)
finally:
	os.chdir(currpath)
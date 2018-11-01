# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os

from shutil import copyfile

inputs_dir = "inputs"

bb_bin = "Poleg_bootblock.bin"
bb_header_xml = "BootBlockAndHeader.xml"
uboot_bin = "u-boot.bin"
uboot_header_xml = "UbootHeader.xml"
uimage_file = "uimage"
uRamdisk_file = "uRamdisk"
dtb_file = "npcm750.dtb"
uboot_env_file = "uboot_env.bin"

def copy_files(src, dest):

	dir_path = os.path.dirname(os.path.realpath(__file__))
	print("copy_files %s" % (dir_path))
	
	dest_file = os.path.join(inputs_dir, dest)

	if not os.path.isdir(inputs_dir):
		os.mkdir(inputs_dir)

	if os.path.isfile(dest_file):
		os.remove(dest_file)

	print("Copy %s to %s" % (src, dest_file))
	copyfile(src, dest_file)

def copy_bootblock_files(BootBlock, BBheader):

	copy_files(BootBlock, bb_bin)
	copy_files(BBheader, bb_header_xml)

def copy_uboot_files(uboot, Ubootheader):

	copy_files(uboot, uboot_bin)
	copy_files(Ubootheader, uboot_header_xml)

def copy_linux_files(uImage, uRamdisk, dtb):

	copy_files(uImage, uimage_file)
	copy_files(uRamdisk, uRamdisk_file)
	copy_files(dtb, dtb_file)

def copy_uboot_env(uboot_env):

	copy_files(uboot_env, uboot_env_file)


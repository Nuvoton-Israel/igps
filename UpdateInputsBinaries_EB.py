# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os

from shutil import copyfile

import ImageGeneration.UpdateInputsBinaries as UpdateInputsBinaries
import ImageGeneration.GenerateImages as GenerateImages


versions_dir = "versions"
ref_dir = "references"

BootBlock_bin_source = os.path.join(versions_dir, "Poleg_bootblock.10.09.02.bin")
BBheader_xml_source = os.path.join(ref_dir, "BootBlockAndHeader_EB.xml")

uboot_bin_source = os.path.join(versions_dir, "u-boot_2015.10.6.9.bin")
Ubootheader_xml_source = os.path.join(ref_dir, "UbootHeader_EB.xml")

linux_image_source = os.path.join(versions_dir, "uimage_4135.01.06")
linux_fs_source = os.path.join(versions_dir, "uRamdisk_4135.01.06")
linux_dtb_source = os.path.join(versions_dir, "nuvoton-npcm750-evb_4135.01.06.dtb")

uboot_env_source = os.path.join(ref_dir, "uboot_env_eb.bin")

currpath = os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:

	
	print("----------------------------------------")
	print("Updating input binaries for Nuvoton's EB")
	print("----------------------------------------")

	os.chdir("ImageGeneration")
	
	if not os.path.isdir(ref_dir):
		os.mkdir(ref_dir)
		
	

	UpdateInputsBinaries.copy_bootblock_files(BootBlock_bin_source, BBheader_xml_source)
	UpdateInputsBinaries.copy_uboot_files(uboot_bin_source, Ubootheader_xml_source)
	UpdateInputsBinaries.copy_linux_files(linux_image_source, linux_fs_source, linux_dtb_source)
	UpdateInputsBinaries.copy_uboot_env(uboot_env_source)

	GenerateImages.run()

except (IOError) as e:
	print("Error Updating input Binaries (%s)" % (e.strerror))
except:
	print("Error Updating input Binaries")
finally:
	os.chdir(currpath)

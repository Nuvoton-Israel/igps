# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os

from shutil import copyfile
from ImageGeneration.version_vars import *

import ImageGeneration.UpdateInputsBinaries
import ImageGeneration.GenerateImages


versions_dir = os.path.join("ImageGeneration", "versions")
ref_dir = os.path.join("ImageGeneration", "references")

BootBlock_bin_source = os.path.join(versions_dir, bootblock_poleg_secure)
BBheader_xml_source = os.path.join(ref_dir, "BootBlockAndHeader_RunBMC.xml")

uboot_bin_source = os.path.join(versions_dir, uboot_poleg)
Ubootheader_xml_source = os.path.join(ref_dir, "UbootHeader_RunBMC.xml")

linux_image_source = os.path.join(versions_dir, linux_uimage_runbmc)
linux_fs_source = os.path.join(versions_dir, linux_uRamdisk_runbmc)
linux_dtb_source = os.path.join(versions_dir, linux_dtb_runbmc)

uboot_env_source = os.path.join(ref_dir, "uboot_env_runbmc.bin")

try:

	print("-----------------------------------------")
	print("Updating input binaries for Nuvoton's RunBMC")
	print("-----------------------------------------")

	if not os.path.isdir(ref_dir):
		os.mkdir(ref_dir)

	ImageGeneration.UpdateInputsBinaries.copy_bootblock_files(BootBlock_bin_source, BBheader_xml_source)
	ImageGeneration.UpdateInputsBinaries.copy_uboot_files(uboot_bin_source, Ubootheader_xml_source)
	ImageGeneration.UpdateInputsBinaries.copy_linux_files(linux_image_source, linux_fs_source, linux_dtb_source)
	ImageGeneration.UpdateInputsBinaries.copy_uboot_env(uboot_env_source)


	print("------------------------------------------------")
	print("Binaries for Nuvoton's RunBMC are ready in 'inputs'")
	print("------------------------------------------------")

except (IOError) as e:
	print("Error Updating input Binaries (%s)" % (e.strerror))
except:
	print("Error Updating input Binaries")

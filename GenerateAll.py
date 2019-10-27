# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import os

import ImageGeneration.GenerateImages

try:
	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	print("==========================================================")
	print("== Generate All Images")
	print("==========================================================")
	ImageGeneration.GenerateImages.run()

except Exception as e:
	pass
finally:
	os.chdir(currpath)
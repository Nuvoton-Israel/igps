# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import os

import ImageGeneration.GenerateImages

try:

	print("==========================================================")
	print("== Generate All Images")
	print("==========================================================")
	ImageGeneration.GenerateImages.run()

except Exception as e:
	pass


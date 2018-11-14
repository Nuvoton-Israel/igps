# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os

def print_error_bad_parameter(function, parameter):
	errorStr = "Error: In %s, '%s' is illegal paramter!" % (function, parameter)
	print("\033[31;1m%s\033[0m") % (errorStr)

def print_error_compare_error(function, c1, c2):
	errorStr = "Error: In %s, %s and %s are not equal!" % (function, c1, c2)
	print("\033[31;1m%s\033[0m") % (errorStr)

def print_error(error_str):
	errorStr = "Error: %s" % (error_str)
	print("\033[31;1m%s\033[0m") % (errorStr)


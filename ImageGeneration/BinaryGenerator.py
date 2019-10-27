# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os


bingo = "bingo"
linux_prefix = "sudo ./"


class BingoError(Exception):

	def __init__(self, value):
		self.strerror = "Bingo error value:" + str(value)
	def __str__(self):
		return repr(self.strerror)


def generate_binary(xmlFile, outputFile):

	_bingo = bingo
	if os.name != "nt":
		_bingo = linux_prefix + bingo
	
	cmd = "%s %s -o %s" % (_bingo, xmlFile, outputFile)

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		rc = os.system(cmd)
		if rc != 0:
			raise BingoError(rc)
	except:
		print("generating %s failed" % (binfile))
		raise
	finally:
		os.chdir(currpath)

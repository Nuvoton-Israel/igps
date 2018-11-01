# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os


signit = "signit"
linux_prefix = "sudo ./"


class SignitError(Exception):

	def __init__(self, value):
		self.strerror = "Signit error value:" + str(value)
	def __str__(self):
		return repr(self.strerror)


def sign_binary(binfile, begin_offset, priv_key, modulu, embed_signature, outputFile):

	_signit = signit
	if os.name != "nt":
		_signit = linux_prefix + signit

	cmd = "%s %s --begin_offset 0x%x --private_key_file %s --modulu_file %s --ebmed_signature 0x%x -o %s -r" \
	% (_signit, binfile, begin_offset, priv_key, modulu, embed_signature, outputFile)

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		rc = os.system(cmd)
		if rc != 0:
			raise SignitError(rc)
	except:
		print("signing %s failed" % (binfile))
		raise
	finally:
		os.chdir(currpath)

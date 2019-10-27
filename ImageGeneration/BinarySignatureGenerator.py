# SPDX-License-Identifier: GPL-2.0
#
# Nuvoton IGPS: Image Generation And Programming Scripts For Poleg BMC
#
# Copyright (C) 2018 Nuvoton Technologies, All Rights Reserved
#-------------------------------------------------------------------------

import sys
import os


def sign_binary(binfile, begin_offset, priv_key, modulu, embed_signature, outputFile):
	
	if os.name != "win32":
		signit_filename = signit + ".exe"

	if os.path.isfile(os.path.join(os.getcwd(), signit_filename)):
		sign_binary_signit(binfile, begin_offset, priv_key, modulu, embed_signature, outputFile)
	else:
		sign_binary_openssl(binfile, begin_offset, priv_key, modulu, embed_signature, outputFile)


signit = "signit"
linux_prefix = "sudo ./"


class SignitError(Exception):

	def __init__(self, value):
		self.strerror = "Signit error value:" + str(value)
	def __str__(self):
		return repr(self.strerror)


def sign_binary_signit(binfile, begin_offset, priv_key, modulu, embed_signature, outputFile):

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


openssl = "openssl"


class OpensslError(Exception):

	def __init__(self, value):
		self.strerror = "Openssl error value:" + str(value)
	def __str__(self):
		return repr(self.strerror)


def convertBinToDER(public, private):

	DER_template_array = ""

	# MODULUS (PUBLIC KEY)
	DER_template_array += "".join(['\x30', '\x82', '\x04', '\xa4', '\x02', '\x01', '\x00', '\x02', '\x82', '\x01', '\x01', '\x00'])
	DER_template_array += public
	
	# PRIVATE EXPONENT
	DER_template_array += "".join(['\x02', '\x03', '\x01', '\x00', '\x01', '\x02', '\x82', '\x01', '\x01', '\x00'])
	DER_template_array += private

	DER_template_array += "".join(['\x02', '\x81', '\x81', '\x00'])	
	DER_template_array += "".join(['\xff']*0x80)

	DER_template_array += "".join(['\x02', '\x81', '\x81', '\x00'])	
	DER_template_array += "".join(['\xff']*0x80)

	DER_template_array += "".join(['\x02', '\x81', '\x80'])	
	DER_template_array += "".join(['\xff']*0x80)

	DER_template_array += "".join(['\x02', '\x81', '\x81', '\x00'])	
	DER_template_array += "".join(['\xff']*0x80)

	DER_template_array += "".join(['\x02', '\x81', '\x80'])	
	DER_template_array += "".join(['\xff']*0x80)

	return DER_template_array


def sign_binary_openssl(bin_filename, begin_offset, privkey_filename, modulu_filename, embed_signature, output_filename):

	_openssl = openssl
	if os.name != "nt":
		_openssl = linux_prefix + openssl

	currpath = os.getcwd()
	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	try:
		signed_area_filename = bin_filename + "_signed_area_file"
		key_filename = "key_file"

		# build temporary file starting from the desired offset of the binfile
		bin_file = open(bin_filename, "rb")
		input = bin_file.read()
		bin_file.close()

		signed_area_file = open(signed_area_filename, "wb")
		signed_area_file.write(input[begin_offset:])
		signed_area_file.close()

		# get keys and build a key in DER format
		module_file = open(modulu_filename, "rb")
		modulus = module_file.read()
		module_file.close()

		privkey_file = open(privkey_filename, "rb")
		privkey = privkey_file.read()
		privkey_file.close()

		key = convertBinToDER(modulus, privkey)

		key_file = open(key_filename, "wb")
		key_file.write(key)
		key_file.close()

		# call openssl to generate a signature
		cmd = "%s dgst -sha256 -binary -keyform der -out %s -sign %s %s" \
		% (_openssl, output_filename, key_filename, signed_area_filename)

		rc = os.system(cmd)
		if rc != 0:
			raise SignitError(rc)

		# get the generated signature and embed it in the input binary
		output_file = open(output_filename, "rb")
		signature = output_file.read()
		output_file.close()

		output = input[:embed_signature] + signature[::-1] + input[(embed_signature + len(signature)):]

		# write the input with the embedded signature to the output file
		output_file = open(output_filename, "wb+")
		output_file.write(output)
		output_file.close()

	except:
		print("signing %s failed" % (bin_filename))
		raise
	finally:
		# remove temporary files
		if os.path.isfile(signed_area_filename):
			os.remove(signed_area_filename)
		if os.path.isfile(key_filename):
			os.remove(key_filename)

		os.chdir(currpath)

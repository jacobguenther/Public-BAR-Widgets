#!/usr/bin/env python3

import os
from hashlib import sha256

current_directory = os.getcwd()

ignore_dirs = [".git", ".github"]

def hash(data_str):
	data_bytes = data_str.encode('utf-8')
	sha256_hash_object = sha256(data_bytes)
	hex_digest = sha256_hash_object.hexdigest()
	return hex_digest

print("dirs")
for dirs in os.listdir():
	# print(subdirs, dirs, files)
	# print("subdirs", subdirs)
	# for subdir in subdirs:
	# 	print(subdir)

	if dir in ignore_dirs:
		print("ignored", dir)
		continue
	print(dir, hash(dir))

	# print("files")
	# for file in files:
	# 	print(file)
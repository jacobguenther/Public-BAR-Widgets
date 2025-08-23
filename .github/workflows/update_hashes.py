#!/usr/bin/env python3

import os

current_directory = os.getcwd()

ignore_dirs = [".git", ".github"]

for subdirs, dirs, files in os.walk(current_directory):
	# print(subdirs, dirs, files)
	# print("subdirs")
	# for subdir in subdirs:
	# 	print(subdir)

	print("dirs")
	for dir in dirs:
		if dir in ignore_dirs:
			continue
		print(dir)

	# print("files")
	# for file in files:
	# 	print(file)
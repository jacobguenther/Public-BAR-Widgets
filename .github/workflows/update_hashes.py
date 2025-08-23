#!/usr/bin/env python3

import os

current_directory = os.getcwd()

for subdirs, dirs, files in os.walk(current_directory):
	# print(subdirs, dirs, files)
	print("subdirs")
	for subdir in subdirs:
		print(subdir)

	print("dirs")
	for dir in dirs:
		print(dir)

	print("files")
	for file in files:
		print(file)
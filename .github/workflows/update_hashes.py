#!/usr/bin/env python3

import os

current_directory = os.getcwd()

for subdirs, dirs, files in os.walk(current_directory):
	print(subdirs, dirs, files)
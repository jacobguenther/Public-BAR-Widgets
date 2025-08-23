import os

for subdirs, dirs, files in os.walk():
	print(subdirs, dirs, files)
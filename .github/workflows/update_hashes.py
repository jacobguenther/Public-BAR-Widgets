#!/usr/bin/env python3

import os
from hashlib import sha256

current_directory = os.getcwd()

ignore_list = [".git", ".github", ".gitmodules", "hashes.txt", "README.md"]

def hash(data_str):
	data_bytes = data_str.encode('utf-8')
	sha256_hash_object = sha256(data_bytes)
	hex_digest = sha256_hash_object.hexdigest()
	return hex_digest

hashes = []

def hash_files_recursive(path):
	print(path, hash(path))

print("dirs")
for file_or_dir in os.listdir():
	if file_or_dir in ignore_list:
		print("ignored", dir)
		continue
	hash_files_recursive(current_directory+"/"+file_or_dir)

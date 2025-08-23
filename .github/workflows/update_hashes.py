#!/usr/bin/env python3

import os
from hashlib import sha256

hashes = []
current_directory = os.getcwd()
ignore_list = [".git", ".github", ".gitmodules", "hashes.txt", "README.md"]

def hash(data_str):
	data_bytes = data_str.encode('utf-8')
	sha256_hash_object = sha256(data_bytes)
	hex_digest = sha256_hash_object.hexdigest()
	return hex_digest

def read_file(path):
	try:
		with open(path, 'r', encoding='utf-8') as file:
			return file.read()
	except FileNotFoundError:
		pass
	except Exception as e:
		pass

def hash_files_recursive(dir_path):
	for file_or_dir in os.listdir(current_directory + "/" + dir_path):
		local_path = dir_path + "/" + file_or_dir
		current_path = current_directory + "/" + local_path

		if os.path.isfile(current_path):
			print("file", current_path)
			file_contents = read_file(current_path)
			if file_contents:
				file_hash = hash(file_contents)
				hashes.append((file_hash, local_path))

		if os.path.isdir(current_path):
			print("dir", current_path)
			hash_files_recursive(local_path)

print("start")

for file_or_dir in os.listdir(current_directory):
	print(file_or_dir)
	if file_or_dir in ignore_list:
		continue
	hash_files_recursive(file_or_dir)

# clear hashes.txt of contents
open(current_directory+"/"+"hashes.txt", "w").close()

# append all the hashes
with open(current_directory+"/"+"hashes.txt", "a") as f:
	for file_hash, file_path in hashes:
		f.write(file_hash+" "+file_path+"\n")
		print(file_hash, file_path)
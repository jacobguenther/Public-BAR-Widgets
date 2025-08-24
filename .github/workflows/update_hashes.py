#!/usr/bin/env python3

import os
import hashlib

hashes = []
ignore_list = [".git", ".github", ".gitignore"]

def hash(data_str):
	data_bytes = data_str.encode('utf-8')
	sha256_hash_object = hashlib.sha256(data_bytes)
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
	for file_or_dir in os.listdir(dir_path):
		current_path = dir_path + "/" + file_or_dir

		if os.path.isfile(current_path) and file_or_dir not in ignore_list:
			file_contents = read_file(current_path)
			if file_contents:
				file_hash = hash(file_contents)
				hashes.append((file_hash, current_path))

		if os.path.isdir(current_path) and file_or_dir not in ignore_list:
			hash_files_recursive(current_path)

def hash_files():
	current_directory = os.getcwd()
	for file_or_dir in os.listdir(current_directory):
		if os.path.isdir(file_or_dir) and file_or_dir not in ignore_list:
			hash_files_recursive(file_or_dir)

def write_hashes():
	open("hashes.txt", "w").close()
	with open("hashes.txt", "a") as f:
		for file_hash, file_path in hashes:
			f.write(file_hash+" "+file_path+"\n")

hash_files()
write_hashes()
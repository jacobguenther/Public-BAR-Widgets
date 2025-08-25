#!/usr/bin/env python3

import os
import hashlib

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

def hash_files_recursive(hashes, dir_path, ignore_list):
	for file_or_dir in os.listdir(dir_path):
		current_path = dir_path + "/" + file_or_dir

		if os.path.isfile(current_path) and file_or_dir not in ignore_list:
			file_contents = read_file(current_path)
			if file_contents:
				file_hash = hash(file_contents)
				hashes.append((file_hash, current_path))

		if os.path.isdir(current_path) and file_or_dir not in ignore_list:
			hash_files_recursive(hashes, current_path, ignore_list)

def hash_files(directory, ignore_list):
	hashes = []
	for file_or_dir in os.listdir(directory):
		hash_files_recursive(hashes, directory+file_or_dir, ignore_list)
	return hashes

def write_hashes(file_path, hashes):
	# clear old hashes
	open(file_path, "w").close()
	with open(file_path, "a") as f:
		for file_hash, file_path in hashes:
			f.write(file_hash+" "+file_path+"\n")

def main():
	# Files in widgets that are ignored
	ignore_list = [".git", ".github", ".gitignore"]
	widget_directory = "Widgets/"
	widget_hashes = hash_files(widget_directory, ignore_list)
	write_hashes("widget_hashes.txt", widget_hashes)

if __name__ == "__main__":
	main()
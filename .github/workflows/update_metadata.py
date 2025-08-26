#!/usr/bin/env python3

import os
import json
import jsonschema
import configparser
import subprocess
import sys

MAX_COVER_IMAGE_SIZE_MB = 4
MAX_COVER_IMAGE_SIZE_X = 1024
MAX_COVER_IMAGE_SIZE_Y = 1024

def read_file(path):
	try:
		with open(path, 'r', encoding='utf-8') as file:
			return file.read(), ""
	except Exception as e:
		return False, f"Error reading file: {e}"

def parse_json(source):
	try:
		return json.loads(source), ""
	except Exception as e:
		return False, f"Error parsing json file: {e}"

def validate_json(data_json, schema_json):
	try:
		jsonschema.validate(instance=data_json, schema=schema_json)
		return True, ""
	except Exception as e:
		return False, f"Error validating json file: {e}"

def parse_submodules(submodules_source):
	submodules = {}
	parser = configparser.ConfigParser()
	parser.read_string(submodules_source)
	for section in parser.sections():
		if section.startswith("submodule "):
			name = section.split('"')[1]
			path = parser.get(section, "path")
			url = parser.get(section, "url")
			submodules[path] = {
				"url": url,
			}
	return submodules
def parse_submodule_status(submoules, result):
	lines = result.stdout.splitlines()
	for line in lines:
		parts = line.strip().split()
		if len(parts) >= 2:
			githash = parts[0].lstrip('-+') # also removes whitespace
			path = parts[1]
			if path in submoules:
				submoules[path]["githash"] = githash
			else:
				raise Exception(f"Submodule path {path} found in status but not in .gitmodules")

def main():
	widget_metadata_schema_src, message = read_file("widget_metadata_schema.json")
	if not widget_metadata_schema_src:
		raise Exception(message)
	widget_metadata_schema_json, message = parse_json(widget_metadata_schema_src)
	if not widget_metadata_schema_json:
		raise Exception(message)

	metadata = []
	for file in os.listdir("widget_metadata"):
		widget_metadata_path = "widget_metadata/"+file
		widget_metadata_src, message = read_file(widget_metadata_path)
		if not widget_metadata_src:
			raise Exception(message)

		widget_metadata_json, message = parse_json(widget_metadata_src)
		if not widget_metadata_json:
			raise Exception(message)

		is_valid, message = validate_json(widget_metadata_json, widget_metadata_schema_json)
		if not is_valid:
			raise Exception(message)
		else:
			print(f"SUCCESS: {widget_metadata_path} is valid according to the schema")

		metadata.append(widget_metadata_json)


	submodules_source, message = read_file(".gitmodules")
	if not submodules_source:
		raise Exception(message)
	
	submodules = parse_submodules(submodules_source)

	result = subprocess.run(["git", "submodule", "status"], capture_output=True, text=True, check=True)
	parse_submodule_status(submodules, result)

	print(submodules)

	seen_display_names = set() # 2 entries can not have the same display name
	seen_submodule_paths = {} # Could 2 entries use the same repo?
	seen_cover_image_paths = {} # Could 2 entries use the same cover image?
	for entry in metadata:
		display_name = entry.get("display_name")
		submodule_path = entry.get("submodule_path")
		cover_image_path = entry.get("cover_image_path")
		# discord_link = entry.get("discord_link")

		if display_name in seen_display_names:
			raise Exception(f"display name conflict: {display_name}")

		if submodule_path in seen_submodule_paths:
			raise Exception(f"submodule path conflict: {submodule_path} for {display_name} and {seen_submodule_paths[submodule_path]}")
		if not os.path.isdir(submodule_path):
			raise Exception(f"missing folder: {submodule_path} for {display_name}")
		
		if submodule_path in submodules:
			entry["github_link"] = submodules.get(submodule_path).get("url")
			entry["githash"] = submodules.get(submodule_path).get("githash")

		if cover_image_path:
			if cover_image_path in seen_cover_image_paths:
				raise Exception(f"cover image path conflict: {cover_image_path} for {display_name} and {seen_cover_image_paths[cover_image_path]}")
			if not os.path.isfile(cover_image_path):
				raise Exception(f"missing cover image file at: {cover_image_path} for {display_name}")
			if os.path.getsize(cover_image_path) / (1024 * 1024) > MAX_COVER_IMAGE_SIZE_MB:
				raise Exception(f"cover image is too large {cover_image_path} must be less than {MAX_COVER_IMAGE_SIZE_MB}")
		
		seen_display_names.add(display_name)
		seen_submodule_paths[submodule_path] = display_name
		seen_cover_image_paths[cover_image_path] = display_name

	for submodule_path in submodules:
		if submodule_path not in seen_submodule_paths:
			raise Exception(f"orphaned submodule {submodule_path}")
	
	if "validate-only" not in sys.argv[1:]:
		with open("widget_metadata.json", "w") as f:
			json.dump(metadata, f, indent="\t")

	print("SUCCESS: widget_metadata.json has no conflicts or missing data")

if __name__ == "__main__":
	main()
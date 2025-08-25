#!/usr/bin/env python3

import os
import json
import jsonschema

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

def main():
	widget_metadata_schema_src, message = read_file("widget_metadata_schema.json")
	if not widget_metadata_schema_src:
		print(message)
		return

	widget_metadata_src, message = read_file("widget_metadata.json")
	if not widget_metadata_src:
		print(message)
		return

	widget_metadata_schema_json, message = parse_json(widget_metadata_schema_src)
	if not widget_metadata_schema_json:
		print(message)
		return

	widget_metadata_json, message = parse_json(widget_metadata_src)
	if not widget_metadata_json:
		print(message)
		return

	is_valid, message = validate_json(widget_metadata_json, widget_metadata_schema_json)
	if not is_valid:
		print(message)
		return
	else:
		print("widget_metadata.json is valid")

if __name__ == "__main__":
	main()
import os
import re

# Load the base path of CPL
BASE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
EXPANDED = []

# Load the content of the header file
def load_header(header: str) -> list[str]:
	try:
		# The path is "<basepath>/src/<header>"
		with open(os.path.join(BASE_PATH, 'src', header), 'r') as f:
			header_source = f.readlines()
	except FileNotFoundError:
		# If the header file is not found, exit
		print(f'ERROR: Header {header} not found')
		exit(0)

	# Load all lines of the header file
	return header_source

def find_indent(line: str) -> str:
	# Find the indentation of the line
	# line.lstrip() return the string after removing the indentation
	return line[ : -len(line.lstrip())]

def expand_header(code: list[str]) -> list[str]:
	patched_code = []

	for line in code:
		try:
			# Find line with the format: '#include "CPL/<header>.hpp"' after removing spaces
			# line.strip().replace(' ', '') removes all endline and whitespace
			# ^ and $ forces the regex to match the entire string
			# (.+?) match any non-empty text (not greedy)
			header_name = re.search('^#include"CPL/(.+?).hpp"$', line.strip().replace(' ', '')).group(1)
		except AttributeError:
			# If the line doesn't have that format, include it normally
			patched_code.append(line)
			continue

		# Save the header names in order to not expand a header twice, which would cause CE
		if header_name in EXPANDED:
			continue

		EXPANDED.append(header_name)

		# Append all lines of the header line with the appropriate indentation
		indentation = find_indent(line)
		# expand_header after loading the header file to resolve chained #includes
		header = [indentation + s for s in expand_header(load_header(header_name + '.hpp'))]

		patched_code += header

	return patched_code
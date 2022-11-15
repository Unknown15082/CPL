import sys
import os

from metadata import load_metadata
from header import expand_header
from escape import escape_end_XML, render_sublime_syntax

def read_stdin():
	try:
		source_code = sys.stdin.readlines()
	except:
		print('ERROR: Unable to read source code')
		exit(0)

	return source_code

def main():
	source_code = read_stdin()
	print("Source Code:\n" + "".join(source_code))

	source_code, data = load_metadata(source_code)
	source_code = expand_header(source_code)
	source_code = escape_end_XML(source_code)
	source_code = render_sublime_syntax(source_code)

	print("Final source code:\n" + "".join(source_code))
	print("Metadata:\n", data)

if __name__ == "__main__":
	main()
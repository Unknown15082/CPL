import sys
import os

from metadata import load_metadata
from header import expand_header
from escape import escape_end_XML, render_sublime_syntax, wrap_headings
from snippet import create_snippet

# Load the base path of CPL
BASE_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

SNIPPET_PATH = os.path.join(BASE_PATH, 'snippets')

def read_stdin() -> str:
	try:
		source_code = sys.stdin.readlines()
	except:
		print('ERROR: Unable to read source code')
		exit(0)

	return source_code

def read_file(filepath: str) -> str:
	try:
		with open(os.path.join(BASE_PATH, filepath), 'r') as f:
			source_code = f.readlines()
	except FileNotFoundError:
		print('ERROR: Unable to read file')
		exit(0)

	return source_code

def main():
	source_code = read_stdin()
	# print("".join(source_code) + "\n" + "-" * 40)

	source_code, data = load_metadata(source_code)
	source_code = expand_header(source_code)
	source_code = escape_end_XML(source_code)
	source_code = render_sublime_syntax(source_code)
	source_code = wrap_headings(source_code, data['Name'])

	# print("".join(source_code) + "\n" + "-" * 40)
	# print("Metadata:\n", data)

	create_snippet(source_code, data, SNIPPET_PATH)

if __name__ == "__main__":
	main()
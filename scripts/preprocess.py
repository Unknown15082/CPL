import sys
import os

def read_input():
	try:
		source_code = sys.stdin.readlines()
	except:
		raise RuntimeError('Unable to read source code')

	return source_code
	
def find_metadata(code: list[str], command: str) -> str:
	for line in code:
		if line.startswith(f'* {command}: '):
			return line[len(f'* {command}: ') : ]

	raise RuntimeError(f'{command} metadata not found')

def load_metadata(code: list[str]) -> tuple[list[str], dict[str, str]]:
	commands = ['Name', 'ShortName', 'Trigger']
	
	try:
		assert(code[0] == '/**\n')
	except AssertionError:
		raise RuntimeError('First line must start with /**')

	try:
		end_metadata = code.index('**/\n')
	except ValueError:
		raise RuntimeError('Cannot find line with **/')

	metadata = code[1 : end_metadata]
	metadata = [line.strip() for line in metadata]

	print("Metadata:\n", metadata)
	data = {}

	for command in commands:
		data[command] = find_metadata(metadata, command)

	if end_metadata + 1 < len(code) and code[end_metadata+1].strip() == '':
		end_metadata += 1
	return code[end_metadata + 1 : ], data

def escape_end_XML(code: list[str]) -> list[str]:
	patched_code = [line.replace(']]>', ']]$NOT_DEFINED>') for line in code]
	return patched_code

def render_sublime_syntax(code: list[str]) -> list[str]:
	patched_code = [line.replace('///***', '') for line in code]
	patched_code = [line.replace('***///', '') for line in patched_code]
	return patched_code

def load_header(header: str) -> list[str]:
	try:
		f = open(os.path.join(os.getcwd(), 'src', header))
	except FileNotFoundError:
		raise RuntimeError(f'Header {header} not found')

	return f.readlines()

def expand_header(code: list[str]) -> list[str]:
	patched_code = []

	INCLUDE_BEGIN = '#include "CPL/'
	INCLUDE_END = '"'

	for line in code:
		if line.strip().startswith(INCLUDE_BEGIN) and line.strip().endswith(INCLUDE_END):
			header = line.strip()[len(INCLUDE_BEGIN) : -len(INCLUDE_END)]

			rep = expand_header(load_header(header))
			patched_code += rep
		else:
			patched_code.append(line)

	return patched_code

def main():
	source_code = read_input()
	print("Source Code:\n" + "".join(source_code))

	source_code, metadata = load_metadata(source_code)
	source_code = expand_header(source_code)
	source_code = escape_end_XML(source_code)
	source_code = render_sublime_syntax(source_code)

	print("Final source code:\n" + "".join(source_code))
	print("Metadata:\n", metadata)

if __name__ == "__main__":
	main()
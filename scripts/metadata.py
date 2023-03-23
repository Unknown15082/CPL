import re

def find_metadata(code: list[str], command: str) -> str:
	for line in code:
		try:
			# Find any line that starts with * <command>
			# ^ and $ forces the regex to match the entire string
			# (.+?) match any non-empty text (not greedy)
			data = re.search(f'^\* {command}: (.+?)$', line.strip()).group(1)
		except AttributeError:
			continue

		return data

	print(f'ERROR: No metadata name {command} found')
	exit(0)

def load_metadata(code: list[str]) -> tuple[list[str], dict[str, str]]:
	# List of metadata
	commands = ['Name', 'Description', 'Trigger']

	try:
		# Assert that the first line of code must be /**, else there is no metadata
		assert(code[0] == '/**\n')
	except AssertionError:
		return code, {}

	try:
		# There must be at least one line with **/
		metadata_endline = code.index('**/\n')
	except ValueError:
		return code, {}

	# Get the metadata
	raw_metadata = code[ : metadata_endline]
	metadata = {}

	for command in commands:
		metadata[command] = find_metadata(code, command)

	# Filter out the remaining source code
	patched_code = code[metadata_endline + 1 : ]

	# If the first line after metadata is empty then remove it
	if len(patched_code) > 0 and patched_code[0].strip() == '':
		patched_code.pop(0)

	return patched_code, metadata

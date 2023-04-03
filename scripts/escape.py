def escape_end_XML(code: list[str]) -> list[str]:
	# ]]> symbol in snippet causes XML syntax error
	patched_code = [line.replace(']]>', ']]$NOT_DEFINED>') for line in code]
	return patched_code

def render_sublime_syntax(code: list[str]) -> list[str]:
	# Escape lines such as /***$0***/
	patched_code = [line.replace('/***', '').replace('***/', '') for line in code]
	return patched_code

def wrap_headings(code: list[str], name: str) -> list[str]:
	# Wrap the code with >>> <name> <<<
	return [f'//=== {name} ===//\n'] + code + [f'\n//=== {name} ===//']
def escape_end_XML(code: list[str]) -> list[str]:
	# ]]> symbol in snippet causes XML syntax error
	patched_code = [line.replace(']]>', ']]$NOT_DEFINED>') for line in code]
	return patched_code

def render_sublime_syntax(code: list[str]) -> list[str]:
	# Escape lines such as /***$0***/
	patched_code = [line.replace('/***', '') for line in code]
	patched_code = [line.replace('***/', '') for line in patched_code]
	return patched_code
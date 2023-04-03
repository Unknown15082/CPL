import os

SNIPPET_FORMAT = '''<snippet>
	<content><![CDATA[
{code}
]]></content>
	<tabTrigger>{trigger}</tabTrigger>
    <description>{description}</description>
	<scope>source.c++</scope>
</snippet>
'''

def create_snippet(code: list[str], metadata: dict[str, str], path: str) -> None:
    snippet = SNIPPET_FORMAT.format(
        code = ''.join(code),
        description = metadata['Description'],
        trigger = metadata['Trigger']
    )

    snippet_name = metadata['Name'].replace(' ', '')

    with open(os.path.join(path, f'{snippet_name}.sublime-snippet'), 'w+') as f:
        f.write(snippet)

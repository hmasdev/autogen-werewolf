from glob import glob
import json
import os
import subprocess
from jinja2 import Environment, FileSystemLoader

# const
WORKDIR: str = '.'
EXAMPLES_DIR: str = 'examples'
README_TEMPLATE_NAME: str = 'README.md.j2'

# vars
readme = Environment(loader=FileSystemLoader(WORKDIR)).get_template(README_TEMPLATE_NAME)  # noqa
help: str = subprocess.run(
    ['python', '-m', 'werewolf', '--help'],
    capture_output=True,
    text=True,
).stdout
examples: dict[str, dict[str, object]] = {
    os.path.splitext(os.path.basename(path).replace('.json', ''))[0]: json.load(open(path))  # noqa
    for path in sorted(glob(os.path.join(EXAMPLES_DIR, '*.json')))
}

# render
print(readme.render(
    help=help,
    examples=[
        example | {'title': f'{name}: {example["title"]}'}
        for name, example in examples.items()
    ],
))

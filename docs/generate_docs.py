from typing import List
from pathlib import Path
import inspect


class DocGenerator:
    def __init__(self, output_dir: str = "docs/api"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_for_class(self, cls):
        doc = inspect.getdoc(cls)
        methods = [
            (name, inspect.getdoc(meth))
            for name, meth in inspect.getmembers(cls, inspect.isfunction)
        ]

        with open(self.output_dir / f"{cls.__name__}.md", "w") as f:
            f.write(f"# {cls.__name__}\n\n{doc}\n\n## Methods\n")
            for name, md in methods:
                f.write(f"### {name}\n\n{md or 'No documentation'}\n\n")
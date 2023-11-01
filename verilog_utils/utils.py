from typing import Callable


def add_indent(line, indent):
    indented_line = "\n".join(f"{indent}\t{part}" for part in line.split("\n"))
    return indented_line

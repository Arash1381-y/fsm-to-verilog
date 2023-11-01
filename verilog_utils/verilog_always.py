from typing import List, Tuple

from verilog_utils.utils import add_indent


def gen_verilog_always(indent: str, triggers: str, statement: str):
    verilog_always = f"{indent}always @({triggers}) begin\n{add_indent(statement, indent)}\n{indent}end\n"
    return verilog_always

from typing import List, Tuple

from verilog_utils.utils import add_indent


def gen_verilog_case(indent: str, var: str, cases: List[Tuple[str, str]]):
    verilog_case = f"{indent}case ({var})\n"
    for case, statement in cases:
        verilog_case += f"{indent}\t{case}: begin\n{add_indent(statement, indent)}\n{indent}\tend\n"
    verilog_case += f"{indent}endcase\n"
    return verilog_case

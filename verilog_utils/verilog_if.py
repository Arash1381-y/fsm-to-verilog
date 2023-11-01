import warnings
from typing import TypeVar, Tuple, List

from verilog_utils.utils import add_indent

ConditionStatement = Tuple[str, str]


def gen_verilog_if_chain(indent: str, *args: ConditionStatement):
    verilog_code = ""

    if args:
        condition, statement = args[0]
        # Generate Verilog code for the first condition
        verilog_code += f"{indent} if ({condition}) begin\n{add_indent(statement, indent)}\n{indent}end "

        # Generate Verilog code for subsequent conditions using elif
        for condition, statement in args[1:]:
            if condition != "":
                verilog_code += f"else if ({condition}) begin\n{add_indent(statement, indent)}\n{indent}end "
            else:
                verilog_code += f"else begin\n{indent}\t{statement}\n{indent}end\n"
                if condition != args[-1][0]:
                    warnings.warn("Warning: 'else' condition found in non-terminal position")
                break

    return verilog_code

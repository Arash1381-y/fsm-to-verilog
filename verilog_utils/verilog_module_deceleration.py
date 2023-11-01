from typing import List, Tuple


def gen_verilog_module_deceleration(module_name: str,
                                    parameters: List[Tuple[str, int]],
                                    inputs: List[Tuple[str | None, str]],
                                    outputs: List[Tuple[str | None, str | None, str]]):
    # set name
    module_declaration: str = f"module {module_name} "

    # set params
    module_declaration += gen_param(parameters)

    if len(outputs) == 0 and len(inputs) == 0:
        module_declaration += ";\n"
        return module_declaration

    # set input, outputs
    module_declaration += '('
    module_declaration += gen_inputs(inputs)

    if len(outputs) == 0:
        module_declaration += ')'
        return module_declaration

    module_declaration += ', '
    module_declaration += gen_outputs(outputs)
    module_declaration += ');\n'

    return module_declaration


def gen_param(parameters: List[Tuple[str, int]]):
    parameters_deceleration = "#("

    for param, def_val in parameters:
        if not def_val:
            raise Exception("No default value for parameter")

        parameters_deceleration += f"parameter {param}={def_val}, "

    # remove last comma
    if len(parameters):
        parameters_deceleration = parameters_deceleration[:- 2]

    parameters_deceleration += ")"

    return parameters_deceleration


def gen_inputs(inputs: List[Tuple[str | None, str]]):
    inputs_deceleration = ""

    for net_size, net_name in inputs:
        if not net_size:
            inputs_deceleration += f"input {net_name}, "
        else:
            inputs_deceleration += f"input {net_size} {net_name}, "

    # remove last comma
    if len(inputs):
        inputs_deceleration = inputs_deceleration[:- 2]

    return inputs_deceleration


def gen_outputs(outputs: List[Tuple[str | None, str | None, str]]):
    output_deceleration = ""

    for sig_type, sig_size, sig_name in outputs:
        output_deceleration += f"output "
        if sig_type == "wire" or sig_type == "reg":
            output_deceleration += f"{sig_type} "
        if sig_size:
            output_deceleration += f"{sig_size} "

        output_deceleration += f"{sig_name}, "

        # remove last comma
    if len(outputs):
        output_deceleration = output_deceleration[:- 2]

    return output_deceleration

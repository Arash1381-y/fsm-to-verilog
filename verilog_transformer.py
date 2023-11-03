import os
from typing import Dict

import config
from fsm_parse import parse_json, extract_nodes, extract_edges
from verilog_utils.verilog_always import gen_verilog_always
from verilog_utils.verilog_case import gen_verilog_case
from verilog_utils.verilog_if import gen_verilog_if_chain
from verilog_utils.verilog_module_deceleration import gen_verilog_module_deceleration


class VerilogTransformer:

    def __init__(self, in_path, out_path):
        self.outputs_net = []
        self.inputs_net = []
        self.out_path = out_path

        data = parse_json(in_path)
        self.nodes = extract_nodes(data)
        self.edges = extract_edges(data)

        self.resolve_output_nets()
        self.resolve_input_nets()

    def run(self):
        functions = [
            self.gen_module_declaration(),
            self.gen_intermediate_signals(),
            self.gen_positive_clock_action(),
            self.gen_next_state_case(),
            self.gen_output()
        ]
        out = '\n'.join(functions) + "endmodule"

        if self.out_path is None:
            print(out)

        else:
            if os.path.exists(self.out_path):
                with open(self.out_path, 'w') as file:
                    file.write(out)
            else:
                # Check if the directory of the file path exists
                directory = os.path.dirname(self.out_path)
                if not os.path.exists(directory):
                    # Create the directory if it does not exist
                    if directory != '':
                        os.makedirs(directory)

                # Create the file if it does not exist
                if not os.path.exists(self.out_path):
                    with open(self.out_path, 'w') as file:
                        file.write(out)

    def resolve_input_nets(self) -> None:
        for l in self.edges.values():
            for edge in l:
                for key in edge.inputs:
                    if key not in self.inputs_net:
                        self.inputs_net.append(key)

    def resolve_output_nets(self) -> None:
        for node in self.nodes.values():
            for key in node.outputs:
                if key not in self.outputs_net:
                    self.outputs_net.append(key)

    def gen_module_declaration(self):
        nodes_num = len(self.nodes)

        in_bits_num = len(self.inputs_net) - 1
        in_net_size = f"[{in_bits_num}:0]" if in_bits_num > 0 else None

        out_bits_num = len(self.outputs_net) - 1
        out_sig_size = f"[{out_bits_num}:0]" if out_bits_num > 0 else None

        return gen_verilog_module_deceleration(
            module_name=config.MODULE_NAME,
            parameters=[("N_STATE", nodes_num)],
            inputs=[
                (None, config.CLOCK_SIG_NAME),
                (None, config.RESET_SIG_NAME),
                (in_net_size, config.IN_NET_SIG_NAME),
            ],
            outputs=[
                ("reg", out_sig_size, config.OUT_REG_SIG_NAME)
            ]
        )

    def gen_intermediate_signals(self):
        intermediate_signals: str = ""
        # define state and next state
        nodes_bits_num = (len(self.nodes) - 1).bit_length() - 1
        if nodes_bits_num <= 0:
            intermediate_signals += (f"reg {config.INTERMEDIATE_CURRENT_STATE_REG_NAME},"
                                     f" {config.INTERMEDIATE_NEXT_STATE_REG_NAME};\n")
        else:
            intermediate_signals += (f"reg [{nodes_bits_num}:0] {config.INTERMEDIATE_CURRENT_STATE_REG_NAME}, "
                                     f"{config.INTERMEDIATE_NEXT_STATE_REG_NAME};\n")

        return intermediate_signals

    @staticmethod
    def gen_positive_clock_action():
        reset_cond, reset_stm = f"{config.RESET_SIG_NAME}", f"{config.INTERMEDIATE_CURRENT_STATE_REG_NAME} <= 0;"
        empty_cond, else_stm = "", (f"{config.INTERMEDIATE_CURRENT_STATE_REG_NAME} <="
                                    f" {config.INTERMEDIATE_NEXT_STATE_REG_NAME};")
        body = gen_verilog_if_chain(
            "\t",
            (reset_cond, reset_stm),
            (empty_cond, else_stm)
        )

        return gen_verilog_always('', f"posedge {config.CLOCK_SIG_NAME}", body)

    def gen_next_state_case(self):
        cases = []
        for node_id, edges in self.edges.items():
            node = self.nodes[node_id]
            if_chain = []
            for edge in edges:
                in_seq = get_seq(src_obj=self.inputs_net, obj=edge.inputs)
                if_case = (
                    f"{config.IN_NET_SIG_NAME} == {in_seq}",
                    f"{config.INTERMEDIATE_NEXT_STATE_REG_NAME} = {self.nodes[edge.dest_id].verilog_id};"
                )
                if_chain.append(if_case)

            cases.append((node.verilog_id, gen_verilog_if_chain('\t', *if_chain)))

        return gen_verilog_always('', f"{config.IN_NET_SIG_NAME} or {config.INTERMEDIATE_CURRENT_STATE_REG_NAME}",
                                  gen_verilog_case('\t', config.INTERMEDIATE_CURRENT_STATE_REG_NAME, cases))

    def gen_output(self):

        cases = []
        for _, node in self.nodes.items():
            out_seq = get_seq(src_obj=self.outputs_net, obj=node.outputs)
            cases.append(
                (
                    f"{config.INTERMEDIATE_CURRENT_STATE_REG_NAME}=={node.verilog_id}",
                    f"{config.OUT_REG_SIG_NAME} = {out_seq};"
                )
            )

        return gen_verilog_always('', f"{config.INTERMEDIATE_CURRENT_STATE_REG_NAME}",
                                  gen_verilog_if_chain('\t', *cases))


def get_seq(src_obj, obj: Dict[str, str]):
    result_seq = ['0'] * len(src_obj)

    for i in range(len(src_obj)):
        name = src_obj[i]
        if name in obj.keys():
            result_seq[i] = obj[name]

    return f"{len(result_seq)}'b" + "".join([str(elem) for elem in result_seq])

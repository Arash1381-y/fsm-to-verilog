from fsm_components.fsm_component import Node


class MooreNode(Node):

    def __init__(self, obj: any, verilog_id):
        super().__init__(obj)
        # if obj does not have key 'output', throw error
        if 'outputs' not in obj:
            raise Exception("Moore node does not have outputs")
        self.outputs = obj['outputs']

        self.verilog_id = verilog_id

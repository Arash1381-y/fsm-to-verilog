from typing import Dict

from fsm_components.fsm_component import Edge


class MooreEdge(Edge):

    def __init__(self, obj: any):
        super().__init__(obj)
        # if obj does not have key 'input', throw error
        if 'inputs' not in obj:
            raise Exception("Moore edge does not have inputs")
        self.inputs: Dict[str, str] = obj['inputs']

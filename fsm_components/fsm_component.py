from abc import ABC, abstractmethod


class FsmComponent(ABC):
    pass


class Node(FsmComponent):
    def __init__(self, obj: any):
        # if obj does not have key 'name', throw error
        if 'name' not in obj:
            raise Exception("Node does not have name")
        self.name = obj['name']

        # if obj does not have key 'node_id', throw error
        if 'node_id' not in obj:
            raise Exception("Node does not have node_id")
        self.node_id = obj['node_id']


class Edge(FsmComponent):
    def __init__(self, obj: any):
        # if obj does not have key 'name', throw error
        if 'name' not in obj:
            raise Exception("Edge does not have name")
        self.name = obj['name']

        # if obj does not have key 'edge_id', throw error
        if 'link_id' not in obj:
            raise Exception("Edge does not have link_id")
        self.edge_id = obj['link_id']

        # if obj does not have key 'source_id', throw error
        if 'source_id' not in obj:
            raise Exception("Edge does not have source_id")
        self.source_id = obj['source_id']

        if 'dest_id' not in obj:
            self.dest_id = obj['source_id']
        else:
            self.dest_id = obj['dest_id']

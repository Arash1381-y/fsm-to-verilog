# Get first arg of command line
import json
import argparse

from typing import List, Dict

from fsm_components.moore.moore_node import MooreNode
from fsm_components.moore.moore_edge import MooreEdge


def parse_json(filename: str) -> any:
    """
    Parses json file and returns data
    """
    # json file
    with open(filename, 'r') as f:
        data = json.load(f)

    return data


def extract_nodes(data: any) -> Dict[str, MooreNode]:
    """
    Extracts nodes from json data

    :param data:  json data
    :return:    list of nodes
    """
    nodes = {}
    bit_len = (len(data['nodes']) - 1).bit_length()
    for node in data['nodes']:
        v_id = set_source_id(len(nodes), bit_len)
        nodes[node['node_id']] = MooreNode(node, v_id)

    return nodes


def extract_edges(data: any) -> Dict[str, List[MooreEdge]]:
    """
    Extracts edges from json data

    :param data: json data
    :return:   list of edges
    """
    edges: Dict[str, List[MooreEdge]] = {}
    for edge in data['links']:
        if edge['source_id'] in edges.keys():
            edges[edge['source_id']].append(MooreEdge(edge))
        else:
            edges[edge['source_id']] = [MooreEdge(edge)]

    return edges


def set_source_id(num, len_bits):
    # Assuming obj['source_id'] is an integer
    binary_string = format(num, f'0{len_bits}b')
    return f"{len_bits}'b{binary_string}"

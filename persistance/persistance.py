import logging
from typing import Union

from models.Graph import Graph, empty_graph
from models.GraphNode import GraphNode
from utils.constants import save_file_path
from utils.error import Error
from utils.file import write_json_to_file, read_json_from_file


def dump_data_to_storage(data: list[Graph]):
    json_data = {
        "graphs": [get_json_from_graph(graph) for graph in data]
    }
    write_json_to_file(json_data, save_file_path)

def load_data_from_storage() -> list[Graph]:
    data = read_json_from_file(save_file_path)
    validation_result = validate_graph_json(data)
    if isinstance(validation_result, Error):
        logging.warning(validation_result)
        return []
    return [graph for graph, _ in [get_graph_from_json(graph) for graph in data["graphs"]]]

def get_json_from_graph(data: Graph):
    return {
        "alias": data.alias,
        "is_directed": data.is_directed,
        "is_weighted": data.is_weighted,
        "nodes": [node.dump() for node in data.nodes],
        "edges": [edge.dump() for edge in data.edges]
    }

def save_graph_to_storage(data: Graph, file_name: str):
    json_data = get_json_from_graph(data)
    write_json_to_file(json_data, file_name)

def get_graph_from_storage(file_name: str) -> tuple[Graph, Error]:
    data = read_json_from_file(file_name)
    return get_graph_from_json(data)

def get_graph_from_json(data: dict) -> tuple[Graph, Error]:
    validation_result = validate_graph_json(data)
    if isinstance(validation_result, Error):
        return empty_graph(), validation_result
    graph = Graph(data["alias"], data["is_directed"], data["is_weighted"])
    for node in data["nodes"]:
        graph.add_node(GraphNode.load(node).name)
    for edge in data["edges"]:
        graph.add_edge(
            edge["source"],
            edge["destination"],
            edge["weight"]
        )
    return graph, Error(0, "")

def validate_graph_json(data: dict) -> Union[bool, Error]:
    if "alias" not in data:
        return Error(1, "alias not found")
    if "is_directed" not in data:
        return Error(1, "is_directed not found")
    if "is_weighted" not in data:
        return Error(1, "is_weighted not found")
    if "nodes" not in data:
        return Error(1, "nodes not found")
    if "edges" not in data:
        return Error(1, "edges not found")
    return True
import logging
from typing import Union
from models.Graph import Graph
from persistance.persistance import load_data_from_storage, get_graph_from_storage, dump_data_to_storage
from utils.error import Error


class GraphRepository:
    def __init__(self, load_from_disk: bool = False):
        self.graphs: dict[str, Graph] = {}
        if load_from_disk:
            self.load()

    def load(self):
        graphs_list = load_data_from_storage()
        graphs = {}
        for graph in graphs_list:
            graphs[graph.alias] = graph
        self.graphs = graphs

    def create_graph(self, alias: str, is_directed: bool = False, is_weighted: bool = False):
        graph = Graph(alias, is_directed, is_weighted)
        self.graphs[alias] = graph

    def create_edge(self, alias: str, node1: str, node2: str, weight: str = "") -> Union[None, Error]:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return Error(1, f"Graph {alias} does not exist")

        if not graph.node_exists(node1):
            return Error(1, f"Node {node1} does not exist in graph {alias}")

        if not graph.node_exists(node2):
            return Error(1, f"Node {node2} does not exist in graph {alias}")

        return graph.add_edge(node1, node2, weight)

    def add_node(self, alias: str, node_name: str) -> Union[None, Error]:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return Error(1, f"Graph {alias} does not exist")
        return self.graphs[alias].add_node(node_name)

    def remove_edge(self, alias: str, node1: str, node2: str, weight: str = "") -> Union[None, Error]:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return Error(1, f"Graph {alias} does not exist")
        return self.graphs[alias].remove_edge(node1, node2, weight)

    def remove_node(self, alias: str, node_name: str) -> Union[None, Error]:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return Error(1, f"Graph {alias} does not exist")
        return self.graphs[alias].remove_node(node_name)

    def get_graph(self, alias: str) -> Union[Error, Graph]:
        if alias not in self.graphs:
            return Error(1, f"Graph {alias} does not exist")
        return self.graphs[alias]

    def graph_exists(self, alias: str) -> bool:
        return alias in self.graphs

    def node_exists(self, alias: str, node_name: str) -> bool:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return False
        return graph.node_exists(node_name)

    def is_weighted(self, alias: str) -> bool:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return False
        return graph.is_weighted

    def is_directed(self, alias: str) -> bool:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return False
        return graph.is_directed

    def list_graphs(self) -> list[str]:
        return list(self.graphs.keys())

    def describe_graph(self, alias)  -> Union[Error, tuple[str, bool, bool]]:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return Error(1, f"Graph {alias} does not exist")
        return graph.alias, graph.is_directed, graph.is_weighted

    def list_nodes(self, alias):
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return Error(1, f"Graph {alias} does not exist")
        return [node.name for node in graph.nodes]

    def list_edges(self, alias: str, node1: str, node2: str):
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return Error(1, f"Graph {alias} does not exist")
        if len(node1) == 0 and len(node2) == 0:
            return [edge.dump() for edge in graph.edges]
        elif len(node1) != 0 and len(node2) != 0:
            return graph.list_edges(node1, node2)
        else:
            return graph.list_edges_for_node(node1 if len(node1) != 0 else node2)

    def load_graph(self, filename: str) -> Union[None, Error]:
        graph, error = get_graph_from_storage(filename)
        if error.is_empty():
            self.graphs[graph.alias] = graph
            return None
        else:
            logging.error(error)
            return error

    def save_all_graphs(self) -> Union[None, Error]:
        try:
            graphs_list = list(self.graphs.values())
            dump_data_to_storage(graphs_list)
            return None
        except Exception as e:
            logging.error(f"Failed to save graphs: {e}")
            return Error(1, f"Failed to save graphs: {str(e)}")

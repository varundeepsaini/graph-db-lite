from typing import Union

from models.Graph import Graph
from repository.GraphRepository import GraphRepository
from utils.error import Error


class GraphService:
    def __init__(self, graph_repository: GraphRepository):
        self.graph_repository = graph_repository

    def create_graph(self, alias: str, is_directed: bool = False, is_weighted: bool = False):
        return self.graph_repository.create_graph(alias, is_directed, is_weighted)

    def create_edge(self, alias: str, node1: str, node2: str, weight: str = "") -> Union[None, Error]:

        if not self.graph_repository.graph_exists(alias):
            return Error(1, f"Graph {alias} does not exist")

        if self.graph_repository.is_weighted(alias) and weight == "":
            return Error(1, "Weight is required for weighted graph")

        if not self.graph_repository.node_exists(alias, node1):
            self.graph_repository.add_node(alias, node1)

        if not self.graph_repository.node_exists(alias, node2):
            self.graph_repository.add_node(alias, node2)

        return self.graph_repository.create_edge(alias, node1, node2, weight)

    def remove_edge(self, alias: str, node1: str, node2: str, weight: str = "") -> Union[None, Error]:
        return self.graph_repository.remove_edge(alias, node1, node2, weight)

    def add_node(self, alias: str, node_name: str) -> Union[None, Error]:
        return self.graph_repository.add_node(alias, node_name)

    def remove_node(self, alias: str, node_name: str) -> Union[None, Error]:
        return self.graph_repository.remove_node(alias, node_name)

    def get_graph(self, alias: str) -> Union[Error, Graph]:
        return self.graph_repository.get_graph(alias)

    def list_graphs(self):
        return self.graph_repository.list_graphs()

    def describe_graph(self, alias: str) -> Union[Error, tuple[str, bool, bool]]:
        return self.graph_repository.describe_graph(alias)

    def list_nodes(self, alias: str) -> Union[Error, list[str]]:
        return self.graph_repository.list_nodes(alias)

    def list_edges(self, alias: str, node1: str, node2: str) -> Union[Error, list]:
        return self.graph_repository.list_edges(alias, node1, node2)

    def node_exists(self, alias: str, node_name: str) -> bool:
        return self.graph_repository.node_exists(alias, node_name)

    def load(self, filename: str):
        return self.graph_repository.load_graph(filename)

    def save_graph(self, alias: str, filename: str) -> Union[None, Error]:
        graph = self.get_graph(alias)
        if isinstance(graph, Error):
            return Error(1, f"Graph {alias} does not exist")
        
        try:
            from persistance.persistance import save_graph_to_storage
            save_graph_to_storage(graph, filename)
            return None
        except Exception as e:
            return Error(1, f"Failed to save graph: {str(e)}")

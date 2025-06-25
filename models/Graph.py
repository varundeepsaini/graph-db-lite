from models.GraphEdge import GraphEdge
from models.GraphNode import GraphNode
from typing import Union
from utils.error import Error

class Graph:
    def __init__(self, alias: str, is_directed: bool=False, is_weighted: bool=False):
        self.nodes_to_index: dict[str, int] = {}
        self.nodes: set[GraphNode] = set()
        self.edges: set[GraphEdge] = set()
        self.adjacency_list: list[set] = []
        self.is_directed: bool = is_directed
        self.is_weighted: bool = is_weighted
        self.alias: str = alias

    def __eq__(self, other):
        if not isinstance(other, Graph):
            return False
        return self.alias == other.alias

    def __hash__(self):
        return hash(self.alias)

    def node_exists(self, name: str) -> bool:
        node = GraphNode(name)
        return node in self.nodes

    def add_node(self, node_name: str) -> Union[None, Error]:
        if self.node_exists(node_name):
            return Error(1, f"Node {node_name} already exists")
        node = GraphNode(node_name)
        self.nodes.add(node)
        self.nodes_to_index[node.name] = len(self.adjacency_list)
        self.adjacency_list.append(set())
        return None

    def add_edge(self, node1_name: str, node2_name: str, weight="") -> Union[None, Error]:
        node1: GraphNode = GraphNode(node1_name)
        node2: GraphNode = GraphNode(node2_name)

        if node1 not in self.nodes:
            return Error(1, f"Node {node1_name} does not exist")
        if node2 not in self.nodes:
            return Error(1, f"Node {node2_name} does not exist")

        if not self.is_weighted:
            weight = 1

        if self.is_weighted and weight == "":
            return Error(1, "Weight is required for weighted graph")

        weight_int = int(weight) if isinstance(weight, str) else weight
        edge = GraphEdge(node1, node2, weight_int)
        if edge in self.edges:
            return Error(1, f"Edge from {node1_name} to {node2_name} already exists")
        self.edges.add(edge)
        self.adjacency_list[self.nodes_to_index[node1.name]].add(edge)
        if not self.is_directed:
            self.adjacency_list[self.nodes_to_index[node2.name]].add(edge)
            return None
        return None

    def remove_edge(self, node1_name: str, node2_name: str, weight="") -> Union[None, Error]:
        node1: GraphNode = GraphNode(node1_name)
        node2: GraphNode = GraphNode(node2_name)

        if node1 not in self.nodes:
            return Error(1, f"Node {node1_name} does not exist")
        if node2 not in self.nodes:
            return Error(1, f"Node {node2_name} does not exist")

        if not self.is_weighted:
            weight = 1

        if self.is_weighted and weight == "":
            return Error(1, "Weight is required for weighted graph")

        weight_int = int(weight) if isinstance(weight, str) else weight
        edge = GraphEdge(node1, node2, weight_int)
        if edge not in self.edges:
            return Error(1, f"Edge from {node1_name} to {node2_name} does not exist")
        self.adjacency_list[self.nodes_to_index[node1.name]].remove(edge)
        self.edges.remove(edge)

        if not self.is_directed:
            rev_edge = GraphEdge(node2, node1, weight_int)
            self.adjacency_list[self.nodes_to_index[node2.name]].remove(rev_edge)
            self.edges.remove(rev_edge)
            return None

        return None

    def dump(self) -> dict:
        return {
            "alias": self.alias,
            "is_directed": self.is_directed,
            "is_weighted": self.is_weighted,
            "nodes": [node.dump() for node in self.nodes],
            "edges": [edge.dump() for edge in self.edges]
        }

    @staticmethod
    def load(data: dict):
        graph = Graph(data["alias"], data["is_directed"], data["is_weighted"])
        for node_data in data["nodes"]:
            graph.add_node(GraphNode.load(node_data).name)
        for edge in data["edges"]:
            graph.add_edge(
                edge["source"],
                edge["destination"],
                edge["weight"]
            )
        return graph

    def list_edges(self, node1_name: str, node2_name: str):
        node1_obj: GraphNode = GraphNode(node1_name)
        node2_obj: GraphNode = GraphNode(node2_name)
        if node1_obj not in self.nodes:
            return Error(1, f"Node {node1_name} does not exist")
        if node2_obj not in self.nodes:
            return Error(1, f"Node {node2_name} does not exist")
        return [edge.dump() for edge in self.adjacency_list[self.nodes_to_index[node1_obj.name]] if edge.destination == node2_obj]

    def list_edges_for_node(self, node_name: str):
        node_obj: GraphNode = GraphNode(node_name)
        if node_obj not in self.nodes:
            return Error(1, f"Node {node_name} does not exist")
        return [edge.dump() for edge in self.adjacency_list[self.nodes_to_index[node_obj.name]]]

    def remove_node(self, node_name: str) -> Union[None, Error]:
        node = GraphNode(node_name)
        if node not in self.nodes:
            return Error(1, f"Node {node_name} does not exist")
        
        edges_to_remove = []
        for edge in self.edges:
            if edge.source == node or edge.destination == node:
                edges_to_remove.append(edge)
        
        for edge in edges_to_remove:
            self.edges.remove(edge)
            if edge.source in self.nodes:
                source_idx = self.nodes_to_index[edge.source.name]
                if edge in self.adjacency_list[source_idx]:
                    self.adjacency_list[source_idx].remove(edge)
            if edge.destination in self.nodes:
                dest_idx = self.nodes_to_index[edge.destination.name]
                if edge in self.adjacency_list[dest_idx]:
                    self.adjacency_list[dest_idx].remove(edge)
        
        self.nodes.remove(node)
        
        self.adjacency_list.clear()
        for i, n in enumerate(self.nodes):
            self.nodes_to_index[n.name] = i
            self.adjacency_list.append(set())
        
        for edge in self.edges:
            if edge.source in self.nodes and edge.destination in self.nodes:
                source_idx = self.nodes_to_index[edge.source.name]
                self.adjacency_list[source_idx].add(edge)
                if not self.is_directed:
                    dest_idx = self.nodes_to_index[edge.destination.name]
                    self.adjacency_list[dest_idx].add(edge)
        
        return None

def empty_graph() -> Graph:
    return Graph("", is_directed=False, is_weighted=False)

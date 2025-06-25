import logging
from typing import List, Callable, Dict
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from repository.GraphRepository import GraphRepository
from service.GraphService import GraphService
from utils.constants import (
    correct_usage_message_add_edge,
    correct_usage_message_add_node,
    CREATE_GRAPH_CMD, ADD_NODE_CMD, ADD_EDGE_CMD, DEL_NODE_CMD, DEL_EDGE_CMD,
    LIST_GRAPHS_CMD, LIST_NODES_CMD, LIST_EDGES_CMD, DESCRIBE_GRAPH_CMD,
    LOAD_GRAPH_CMD, SAVE_GRAPH_CMD, HELP_CMD, EXIT_CMD, CLEAR_CMD,
    GRAPH_ALREADY_EXISTS, GRAPH_DOES_NOT_EXIST, NO_GRAPHS_EXIST, NO_NODES_IN_GRAPH,
    NO_EDGES_FOUND, FAILED_TO_LOAD_GRAPH, GRAPH_CREATED, NODE_ADDED,
    EDGE_ADDED, EDGE_REMOVED, GRAPH_LOADED, NODE_REMOVED, GRAPH_SAVED, AVAILABLE_GRAPHS,
    NODES_IN_GRAPH, EDGES_IN_GRAPH, GRAPH_INFO, DIRECTED_INFO,
    WEIGHTED_INFO, NODES_COUNT, EDGES_COUNT, HELP_TEXT
)
from utils.error import Error
from validators.graph_validators import (
    validate_add_edge, validate_add_node, validate_create_graph,
    validate_delete_node, validate_delete_edge, validate_list_nodes,
    validate_list_edges, validate_describe_graph, validate_load_graph,
    validate_save_graph
)
from utils.config import get_save_file_path

class GraphDBLiteCLI:
    def __init__(self):
        self.repository = GraphRepository(load_from_disk=True)
        self.service = GraphService(self.repository)
        self.commands = [
            CREATE_GRAPH_CMD, ADD_NODE_CMD, ADD_EDGE_CMD, DEL_NODE_CMD, DEL_EDGE_CMD,
            LIST_GRAPHS_CMD, LIST_NODES_CMD, LIST_EDGES_CMD, DESCRIBE_GRAPH_CMD,
            LOAD_GRAPH_CMD, SAVE_GRAPH_CMD, HELP_CMD, EXIT_CMD, CLEAR_CMD
        ]
        self.completer = WordCompleter(self.commands, ignore_case=True)
        self.style = Style.from_dict({
            'prompt': 'ansicyan bold',
            'error': 'ansired bold',
            'success': 'ansigreen bold',
            'info': 'ansiblue bold',
            'warning': 'ansiyellow bold'
        })
        # Command map for dispatch
        self.command_map: Dict[str, Callable[[List[str]], bool]] = {
            CREATE_GRAPH_CMD: self.handle_create_graph,
            ADD_NODE_CMD: self.handle_add_node,
            ADD_EDGE_CMD: self.handle_add_edge,
            DEL_NODE_CMD: self.handle_delete_node,
            DEL_EDGE_CMD: self.handle_delete_edge,
            LIST_GRAPHS_CMD: self.handle_list_graphs,
            LIST_NODES_CMD: self.handle_list_nodes,
            LIST_EDGES_CMD: self.handle_list_edges,
            DESCRIBE_GRAPH_CMD: self.handle_describe_graph,
            LOAD_GRAPH_CMD: self.handle_load_graph,
            SAVE_GRAPH_CMD: self.handle_save_graph,
            HELP_CMD: self.show_help_command,
            CLEAR_CMD: self.clear_command,
            EXIT_CMD: self.exit_command
        }
        self.should_exit = False

    def print_error(self, message: str):
        print(f"\033[91mERROR: {message}\033[0m")

    def print_success(self, message: str):
        print(f"\033[92mSUCCESS: {message}\033[0m")

    def print_info(self, message: str):
        print(f"\033[94mINFO: {message}\033[0m")

    def print_warning(self, message: str):
        print(f"\033[93mWARNING: {message}\033[0m")

    def show_help(self):
        print(HELP_TEXT)

    def show_help_command(self, args: List[str]) -> bool:
        self.show_help()
        return True

    def clear_command(self, args: List[str]) -> bool:
        print("\033[2J\033[H")
        return True

    def exit_command(self, args: List[str]) -> bool:
        self.should_exit = True
        return False

    def graceful_shutdown(self):
        try:
            graphs = self.service.list_graphs()
            if graphs:
                self.print_info("Saving all graphs to disk...")
                result = self.service.save_all_graphs()
                if isinstance(result, Error):
                    self.print_error(f"Failed to save graphs: {result.message}")
                else:
                    self.print_success(f"Successfully saved {len(graphs)} graph(s) to disk")
            else:
                self.print_info("No graphs to save")
        except Exception as e:
            self.print_error(f"Error during shutdown: {str(e)}")
            logging.error(f"Error during graceful shutdown: {e}")

    def parse_command(self, command: str) -> tuple[str, List[str]]:
        parts = command.strip().split()
        if not parts:
            return "", []
        for n in range(len(parts), 0, -1):
            candidate = " ".join([p.upper() for p in parts[:n]])
            if candidate in self.command_map:
                return candidate, parts[n:]
        return parts[0].upper(), parts[1:]

    def handle_create_graph(self, args: List[str]) -> bool:
        validation_result = validate_create_graph(args)
        if isinstance(validation_result, Error):
            self.print_error(validation_result.message)
            return False
        alias = args[0]
        is_directed = "DIRECTED" in [arg.upper() for arg in args[1:]]
        is_weighted = "WEIGHTED" in [arg.upper() for arg in args[1:]]
        existing_graph = self.service.get_graph(alias)
        if not isinstance(existing_graph, Error):
            self.print_error(GRAPH_ALREADY_EXISTS.format(alias=alias))
            return False
        self.service.create_graph(alias, is_directed, is_weighted)
        self.print_success(GRAPH_CREATED.format(alias=alias, directed=is_directed, weighted=is_weighted))
        return True

    def handle_add_node(self, args: List[str]) -> bool:
        validation_result = validate_add_node(args)
        if isinstance(validation_result, Error):
            self.print_error(correct_usage_message_add_node)
            return False
        graph_alias, node_name = args[0], args[1]
        existing_graph = self.service.get_graph(graph_alias)
        if isinstance(existing_graph, Error):
            self.print_error(GRAPH_DOES_NOT_EXIST.format(alias=graph_alias))
            return False
        result = self.service.add_node(graph_alias, node_name)
        if isinstance(result, Error):
            self.print_error(result.message)
            return False
        self.print_success(NODE_ADDED.format(node=node_name, alias=graph_alias))
        return True

    def handle_add_edge(self, args: List[str]) -> bool:
        validation_result = validate_add_edge(args)
        if isinstance(validation_result, Error):
            self.print_error(correct_usage_message_add_edge)
            return False
        graph_alias, node1, node2 = args[0], args[1], args[2]
        weight = args[3] if len(args) > 3 else ""
        existing_graph = self.service.get_graph(graph_alias)
        if isinstance(existing_graph, Error):
            self.print_error(GRAPH_DOES_NOT_EXIST.format(alias=graph_alias))
            return False
        result = self.service.create_edge(graph_alias, node1, node2, weight)
        if isinstance(result, Error):
            self.print_error(result.message)
            return False
        weight_text = f" with weight {weight}" if weight else ""
        self.print_success(EDGE_ADDED.format(node1=node1, node2=node2, weight_text=weight_text, alias=graph_alias))
        return True

    def handle_delete_node(self, args: List[str]) -> bool:
        validation_result = validate_delete_node(args)
        if isinstance(validation_result, Error):
            self.print_error(validation_result.message)
            return False
        graph_alias, node_name = args[0], args[1]
        existing_graph = self.service.get_graph(graph_alias)
        if isinstance(existing_graph, Error):
            self.print_error(GRAPH_DOES_NOT_EXIST.format(alias=graph_alias))
            return False
        result = self.service.remove_node(graph_alias, node_name)
        if isinstance(result, Error):
            self.print_error(result.message)
            return False
        self.print_success(NODE_REMOVED.format(node=node_name, alias=graph_alias))
        return True

    def handle_delete_edge(self, args: List[str]) -> bool:
        validation_result = validate_delete_edge(args)
        if isinstance(validation_result, Error):
            self.print_error(validation_result.message)
            return False
        graph_alias, node1, node2 = args[0], args[1], args[2]
        weight = args[3] if len(args) > 3 else ""
        existing_graph = self.service.get_graph(graph_alias)
        if isinstance(existing_graph, Error):
            self.print_error(GRAPH_DOES_NOT_EXIST.format(alias=graph_alias))
            return False
        result = self.service.remove_edge(graph_alias, node1, node2, weight)
        if isinstance(result, Error):
            self.print_error(result.message)
            return False
        weight_text = f" with weight {weight}" if weight else ""
        self.print_success(EDGE_REMOVED.format(node1=node1, node2=node2, weight_text=weight_text, alias=graph_alias))
        return True

    def handle_list_graphs(self, args: List[str]) -> bool:
        graphs = self.service.list_graphs()
        if not graphs:
            self.print_info(NO_GRAPHS_EXIST)
            return True
        self.print_info(AVAILABLE_GRAPHS)
        for graph_alias in graphs:
            print(f"  - {graph_alias}")
        return True

    def handle_list_nodes(self, args: List[str]) -> bool:
        validation_result = validate_list_nodes(args)
        if isinstance(validation_result, Error):
            self.print_error(validation_result.message)
            return False
        graph_alias = args[0]
        existing_graph = self.service.get_graph(graph_alias)
        if isinstance(existing_graph, Error):
            self.print_error(GRAPH_DOES_NOT_EXIST.format(alias=graph_alias))
            return False
        result = self.service.list_nodes(graph_alias)
        if isinstance(result, Error):
            self.print_error(result.message)
            return False
        if not result:
            self.print_info(NO_NODES_IN_GRAPH.format(alias=graph_alias))
            return True
        self.print_info(NODES_IN_GRAPH.format(alias=graph_alias))
        for node in result:
            print(f"  - {node}")
        return True

    def handle_list_edges(self, args: List[str]) -> bool:
        validation_result = validate_list_edges(args)
        if isinstance(validation_result, Error):
            self.print_error(validation_result.message)
            return False
        graph_alias = args[0]
        node1 = args[1] if len(args) > 1 else ""
        node2 = args[2] if len(args) > 2 else ""
        existing_graph = self.service.get_graph(graph_alias)
        if isinstance(existing_graph, Error):
            self.print_error(GRAPH_DOES_NOT_EXIST.format(alias=graph_alias))
            return False
        result = self.service.list_edges(graph_alias, node1, node2)
        if isinstance(result, Error):
            self.print_error(result.message)
            return False
        if not result:
            self.print_info(NO_EDGES_FOUND.format(alias=graph_alias))
            return True
        self.print_info(EDGES_IN_GRAPH.format(alias=graph_alias))
        for edge in result:
            if isinstance(edge, dict):
                source = edge.get('source', 'Unknown')
                destination = edge.get('destination', 'Unknown')
                weight = edge.get('weight', '1')
                print(f"  - {source} -> {destination} (weight: {weight})")
            else:
                print(f"  - {edge}")
        return True

    def handle_describe_graph(self, args: List[str]) -> bool:
        validation_result = validate_describe_graph(args)
        if isinstance(validation_result, Error):
            self.print_error(validation_result.message)
            return False
        graph_alias = args[0]
        result = self.service.describe_graph(graph_alias)
        if isinstance(result, Error):
            self.print_error(result.message)
            return False
        alias, is_directed, is_weighted = result
        self.print_info(GRAPH_INFO.format(alias=alias))
        print(DIRECTED_INFO.format(directed=is_directed))
        print(WEIGHTED_INFO.format(weighted=is_weighted))
        nodes_result = self.service.list_nodes(graph_alias)
        if not isinstance(nodes_result, Error):
            print(NODES_COUNT.format(count=len(nodes_result)))
        edges_result = self.service.list_edges(graph_alias, "", "")
        if not isinstance(edges_result, Error):
            print(EDGES_COUNT.format(count=len(edges_result)))
        return True

    def handle_load_graph(self, args: List[str]) -> bool:
        validation_result = validate_load_graph(args)
        if isinstance(validation_result, Error):
            self.print_error(validation_result.message)
            return False
        filename = args[0]
        result = self.service.load(filename)
        if isinstance(result, Error):
            self.print_error(FAILED_TO_LOAD_GRAPH.format(message=result.message))
            return False
        self.print_success(GRAPH_LOADED.format(filename=filename))
        return True

    def handle_save_graph(self, args: List[str]) -> bool:
        validation_result = validate_save_graph(args)
        if isinstance(validation_result, Error):
            self.print_error(validation_result.message)
            return False
        graph_alias, filename = args[0], args[1]
        existing_graph = self.service.get_graph(graph_alias)
        if isinstance(existing_graph, Error):
            self.print_error(GRAPH_DOES_NOT_EXIST.format(alias=graph_alias))
            return False
        result = self.service.save_graph(graph_alias, filename)
        if isinstance(result, Error):
            self.print_error(result.message)
            return False
        self.print_success(GRAPH_SAVED.format(alias=graph_alias, filename=filename))
        return True

    def load_graphs(self):
        self.service.load_graphs()

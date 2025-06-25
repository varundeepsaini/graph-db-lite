from utils.config import get_save_file_path

save_file_path: str = get_save_file_path()

error_message_invalid_input = "Invalid input"


invalid_command_message_tooltip = "Available commands are: ADD NODE, ADD EDGE, DEL NODE"
correct_usage_message_add_edge = "Correct usage: \nADD EDGE <graph_alias> <node1> <node2> <weight>(if given when initializing graph) \ngraph_alias node1 and node2 should be alphanumeric (A-Z, a-z, 0-9 and no spaces) and weight should be numeric"
correct_usage_message_add_node = "Correct usage: \nADD NODE <graph_alias> <node_name> \ngraph_alias and node_name should be alphanumeric (A-Z, a-z, 0-9 and no spaces)"
correct_usage_message_delete_node = "Correct usage: \nDEL NODE <graph_alias> <node_name> \ngraph_alias and node_name should be alphanumeric (A-Z, a-z, 0-9 and no spaces)"

CREATE_GRAPH_CMD = "CREATE GRAPH"
ADD_NODE_CMD = "ADD NODE"
ADD_EDGE_CMD = "ADD EDGE"
DEL_NODE_CMD = "DEL NODE"
DEL_EDGE_CMD = "DEL EDGE"
LIST_GRAPHS_CMD = "LIST GRAPHS"
LIST_NODES_CMD = "LIST NODES"
LIST_EDGES_CMD = "LIST EDGES"
DESCRIBE_GRAPH_CMD = "DESCRIBE GRAPH"
LOAD_GRAPH_CMD = "LOAD GRAPH"
SAVE_GRAPH_CMD = "SAVE GRAPH"
HELP_CMD = "HELP"
EXIT_CMD = "EXIT"
CLEAR_CMD = "CLEAR"

WELCOME_MESSAGE = "Welcome to GraphDBLite!"
HELP_PROMPT = "Type 'HELP' for available commands or 'EXIT' to quit."
GOODBYE_MESSAGE = "Goodbye!"
USE_EXIT_MESSAGE = "Use 'EXIT' to quit."

GRAPH_ALREADY_EXISTS = "Graph '{alias}' already exists"
GRAPH_DOES_NOT_EXIST = "Graph '{alias}' does not exist"
NODE_DELETION_NOT_IMPLEMENTED = "Node deletion not yet implemented"
GRAPH_SAVING_NOT_IMPLEMENTED = "Graph saving not yet implemented"
NO_GRAPHS_EXIST = "No graphs exist"
NO_NODES_IN_GRAPH = "No nodes in graph '{alias}'"
NO_EDGES_FOUND = "No edges found in graph '{alias}'"
FAILED_TO_LOAD_GRAPH = "Failed to load graph: {message}"

GRAPH_CREATED = "Created graph '{alias}' (directed: {directed}, weighted: {weighted})"
NODE_ADDED = "Added node '{node}' to graph '{alias}'"
EDGE_ADDED = "Added edge from '{node1}' to '{node2}'{weight_text} in graph '{alias}'"
EDGE_REMOVED = "Removed edge from '{node1}' to '{node2}'{weight_text} in graph '{alias}'"
GRAPH_LOADED = "Loaded graph from '{filename}'"
NODE_REMOVED = "Removed node '{node}' from graph '{alias}'"
GRAPH_SAVED = "Saved graph '{alias}' to '{filename}'"

AVAILABLE_GRAPHS = "Available graphs:"
NODES_IN_GRAPH = "Nodes in graph '{alias}':"
EDGES_IN_GRAPH = "Edges in graph '{alias}':"
GRAPH_INFO = "Graph: {alias}"
DIRECTED_INFO = "  Directed: {directed}"
WEIGHTED_INFO = "  Weighted: {weighted}"
NODES_COUNT = "  Nodes: {count}"
EDGES_COUNT = "  Edges: {count}"

CREATE_GRAPH_USAGE = "Usage: CREATE GRAPH <alias> [DIRECTED] [WEIGHTED]"
LIST_NODES_USAGE = "Usage: LIST NODES <graph_alias>"
LIST_EDGES_USAGE = "Usage: LIST EDGES <graph_alias> [node1] [node2]"
DESCRIBE_GRAPH_USAGE = "Usage: DESCRIBE GRAPH <graph_alias>"
LOAD_GRAPH_USAGE = "Usage: LOAD GRAPH <filename>"
SAVE_GRAPH_USAGE = "Usage: SAVE GRAPH <graph_alias> <filename>"
DEL_EDGE_USAGE = "Usage: DEL EDGE <graph_alias> <node1> <node2> [weight]"

HELP_TEXT = """
GraphDBLite - Lightweight Graph Database

Available Commands:
==================

Graph Management:
  CREATE GRAPH <alias> [DIRECTED] [WEIGHTED]  - Create a new graph
  LIST GRAPHS                                 - List all graphs
  DESCRIBE GRAPH <alias>                      - Show graph properties
  LOAD GRAPH <filename>                       - Load graph from file
  SAVE GRAPH <alias> <filename>               - Save graph to file

Node Operations:
  ADD NODE <graph_alias> <node_name>          - Add a node to graph
  DEL NODE <graph_alias> <node_name>          - Delete a node from graph
  LIST NODES <graph_alias>                    - List all nodes in graph

Edge Operations:
  ADD EDGE <graph_alias> <node1> <node2> [weight]  - Add an edge
  DEL EDGE <graph_alias> <node1> <node2> [weight]  - Delete an edge
  LIST EDGES <graph_alias> [node1] [node2]         - List edges

Utility:
  HELP                                         - Show this help
  CLEAR                                        - Clear screen
  EXIT                                         - Exit application

Examples:
  CREATE GRAPH social DIRECTED
  ADD NODE social alice
  ADD EDGE social alice bob 5
  LIST NODES social
"""
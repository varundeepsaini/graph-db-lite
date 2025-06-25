from typing import Union
from utils.constants import (
    error_message_invalid_input,
    CREATE_GRAPH_USAGE,
    LIST_NODES_USAGE,
    LIST_EDGES_USAGE,
    DESCRIBE_GRAPH_USAGE,
    LOAD_GRAPH_USAGE,
    SAVE_GRAPH_USAGE,
    DEL_EDGE_USAGE,
    correct_usage_message_delete_node
)
from utils.error import Error

def validate_add_edge(args: list[str]) -> Union[bool, Error]:
    if len(args) < 3 or len(args) > 4:
        return Error(1, error_message_invalid_input)

    if len(args) == 4 and not args[3].isnumeric():
        return Error(1, error_message_invalid_input)

    for arg in args[:3]:
        if not arg.isalnum():
            return Error(1, error_message_invalid_input)

    return True

def validate_add_node(args: list[str]) -> Union[bool, Error]:
    if len(args) != 2:
        return Error(1, error_message_invalid_input)

    for arg in args:
        if not arg.isalnum():
            return Error(1, error_message_invalid_input)

    return True

def validate_create_graph(args: list[str]) -> Union[bool, Error]:
    if len(args) < 1:
        return Error(1, CREATE_GRAPH_USAGE)
    
    if not args[0].isalnum():
        return Error(1, error_message_invalid_input)
    
    valid_flags = {"DIRECTED", "WEIGHTED"}
    for arg in args[1:]:
        if arg.upper() not in valid_flags:
            return Error(1, error_message_invalid_input)
    
    return True

def validate_delete_node(args: list[str]) -> Union[bool, Error]:
    if len(args) != 2:
        return Error(1, correct_usage_message_delete_node)
    
    for arg in args:
        if not arg.isalnum():
            return Error(1, error_message_invalid_input)
    
    return True

def validate_delete_edge(args: list[str]) -> Union[bool, Error]:
    if len(args) < 3 or len(args) > 4:
        return Error(1, DEL_EDGE_USAGE)
    
    for arg in args[:3]:
        if not arg.isalnum():
            return Error(1, error_message_invalid_input)
    
    if len(args) == 4 and not args[3].isnumeric():
        return Error(1, error_message_invalid_input)
    
    return True

def validate_list_nodes(args: list[str]) -> Union[bool, Error]:
    if len(args) != 1:
        return Error(1, LIST_NODES_USAGE)
    
    if not args[0].isalnum():
        return Error(1, error_message_invalid_input)
    
    return True

def validate_list_edges(args: list[str]) -> Union[bool, Error]:
    if len(args) < 1 or len(args) > 3:
        return Error(1, LIST_EDGES_USAGE)
    
    if not args[0].isalnum():
        return Error(1, error_message_invalid_input)
    
    for arg in args[1:]:
        if not arg.isalnum():
            return Error(1, error_message_invalid_input)
    
    return True

def validate_describe_graph(args: list[str]) -> Union[bool, Error]:
    if len(args) != 1:
        return Error(1, DESCRIBE_GRAPH_USAGE)
    
    if not args[0].isalnum():
        return Error(1, error_message_invalid_input)
    
    return True

def validate_load_graph(args: list[str]) -> Union[bool, Error]:
    if len(args) != 1:
        return Error(1, LOAD_GRAPH_USAGE)
    
    if not args[0].strip():
        return Error(1, error_message_invalid_input)
    
    return True

def validate_save_graph(args: list[str]) -> Union[bool, Error]:
    if len(args) != 2:
        return Error(1, SAVE_GRAPH_USAGE)
    
    if not args[0].isalnum():
        return Error(1, error_message_invalid_input)
    
    if not args[1].strip():
        return Error(1, error_message_invalid_input)
    
    return True



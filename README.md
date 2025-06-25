# GraphDBLite

A lightweight, persistent graph database with a command-line interface for creating, managing, and visualizing graphs.

## What it does

GraphDBLite allows you to:
- Create directed/undirected and weighted/unweighted graphs
- Add and remove nodes and edges
- List and describe graphs
- Save graphs to disk and load them back
- Persistent storage with automatic graceful shutdown

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root:
```
SAVE_FILE_PATH=/path/to/your/graphs.json
```

This variable specifies where all graphs will be saved by default.

## Running the application

```bash
python main.py
```

## Commands

### Graph Management
- `CREATE GRAPH <alias> [DIRECTED] [WEIGHTED]` - Create a new graph
- `LIST GRAPHS` - List all graphs
- `DESCRIBE GRAPH <alias>` - Show graph properties
- `LOAD GRAPH <filename>` - Load graph from file
- `SAVE GRAPH <alias> <filename>` - Save graph to file

### Node Operations
- `ADD NODE <graph_alias> <node_name>` - Add a node to graph
- `DEL NODE <graph_alias> <node_name>` - Delete a node from graph
- `LIST NODES <graph_alias>` - List all nodes in graph

### Edge Operations
- `ADD EDGE <graph_alias> <node1> <node2> [weight]` - Add an edge
- `DEL EDGE <graph_alias> <node1> <node2> [weight]` - Delete an edge
- `LIST EDGES <graph_alias> [node1] [node2]` - List edges

### Utility
- `HELP` - Show help
- `CLEAR` - Clear screen
- `EXIT` - Exit application

## Examples

```
CREATE GRAPH social DIRECTED
ADD NODE social alice
ADD NODE social bob
ADD EDGE social alice bob 5
LIST NODES social
DESCRIBE GRAPH social
EXIT
```

## Graceful Shutdown

The application automatically saves all graphs to disk when you exit using `EXIT` or Ctrl+C. No data is lost. 
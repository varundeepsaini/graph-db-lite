from models.GraphNode import GraphNode

class GraphEdge:
    def __init__(self, source: GraphNode, destination: GraphNode, weight=1):
        self.source = source
        self.destination = destination
        self.weight = weight

    def __eq__(self, other):
        if not isinstance(other, GraphEdge):
            return False
        return (self.source == other.source and
                self.destination == other.destination and
                self.weight == other.weight)

    def __hash__(self):
        return hash((self.source, self.destination, self.weight))

    def clone(self):
        return GraphEdge(self.source, self.destination, self.weight)

    def dump(self):
        return {
            "source": self.source.name,
            "destination": self.destination.name,
            "weight": self.weight
        }

    @staticmethod
    def load(data: dict):
        if isinstance(data["source"], str):
            source_node = GraphNode(data["source"])
        else:
            source_node = GraphNode.load(data["source"])
            
        if isinstance(data["destination"], str):
            destination_node = GraphNode(data["destination"])
        else:
            destination_node = GraphNode.load(data["destination"])
            
        return GraphEdge(source_node, destination_node, data["weight"])

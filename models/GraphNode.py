class GraphNode:
    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, GraphNode):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def clone(self):
        return GraphNode(self.name)

    def dump(self):
        return {
            "name": self.name
        }

    @staticmethod
    def load(data: dict):
        return GraphNode(data["name"])
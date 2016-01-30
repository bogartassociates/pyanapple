class NodeManager:

    nodes = []

    def __init__(self, cluster):
        self.name = cluster

    def join(self, node):
        self.nodes.append(node)

    def leave(self, node):
        self.nodes.remove(node)

    def cluster(self, detail=False):
        if detail == True:
            for node in self.nodes:
                print(node.details)
        else:
            stats = {}
            stats['nodes'] = len(self.nodes)
            stats['name'] = self.name
            return stats
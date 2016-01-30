class NodeManager:

    nodes = []

    def __init__(self, cluster):
        self.name = cluster

    def join(self, node):
        self.nodes.append(node)

    def leave(self, node):
        self.nodes.remove(node)

    def cluster(self, pretty):
        if pretty == True:
            for node in self.nodes:
                print(node.details)
        else:
            nodes
            for node in self.nodes:
                nodes.append(node)
            return nodes


class NodeManager:

    nodes = []

    def __init__(self, cluster):
        self.name = cluster

    def join(self, candidate):
        if candidate.details['name'] not in set(node['name'] for node in self.cluster(detail=True)):
            self.nodes.append(candidate)
            return candidate.details['name'] + ' has joined ' + self.name
        return candidate.details['name'] + ' is already a member of ' + self.name

    def leave(self, member):
        for node in self.nodes:
            if node.details['name'] == member.details['name']:
                self.nodes.remove(node)
                return node.details['name'] + ' removed from ' + self.name
        return "node not found"

    def cluster(self, detail=False):
        if detail == True:
            output = []
            for node in self.nodes:
                output.append(node.details)
            return output
        else:
            stats = {}
            stats['nodes'] = len(self.nodes)
            stats['cluster_name'] = self.name
            stats['node_names'] = list(set(node['name'] for node in self.cluster(detail=True)))
            return stats
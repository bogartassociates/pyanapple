def basic():
    from securitymesh import Node
    from securitymesh import NodeManager

    node1 = Node(1,2,3,4)
    node2 = Node(5,6,7,8)
    smesh = NodeManager('shield')
    smesh.join(node1)
    smesh.join(node2)
    print("created cluster 'smesh'")
    return smesh
# NodeTypeList: Simple String List in Python, This is the list of Nodes that you want to create, Each Element in this List is bl_idname of Nodes a.k.a types
# NodeTree: The NodeTree It's Gonna Be Created in
# Gap: When Multiple Nodes, Gap Between them [NOT MARGIN]
# Will always create Nodes in LeftToRight Order 
# TODO: Maybe add Top To Bottom Support
def AddNodesAtCenter(NodeTypeList, NodeTree, Gap):
    if len(NodeTypeList) == 1:
        newNode = NodeTree.nodes.new(type = NodeTypeList[0])
        newNode.location = nodeTree.view_center
        return

    centerX = nodeTree.view_center[0]
    centerY = nodeTree.view_center[1]
    totalWidth = -Gap
    NodeList = []

    for Node in NodeTypeList:
        newNode = NodeTree.nodes.new(type = Node)

        NodeList.append(newNode)
        totalWidth += (newNode.width + Gap)

    for Node in NodeList:
        w = Node.width
        posX = nextPos + (w / 2)
        Node.location = (posX, centerY)

        nextPos += w + Gap
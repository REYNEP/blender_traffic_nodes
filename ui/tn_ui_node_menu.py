from nodeitems_utils import NodeCategory, NodeItem, register_node_categories, unregister_node_categories

class TrafficNodesCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'TrafficNodeTreeType'
            
        

nodeCategories = [
    TrafficNodesCategory("INPUTNODES", "Input Nodes", items = [
        NodeItem("ObjectSelectionNode")
    ]),
    TrafficNodesCategory("GODSEYES", "God's Eye's", items = [
        NodeItem("ViewerNode")
    ])
]

def getNodeCategories():
    #TODO Implement a Dictionary / LIST Of Nodes then Load those into nodeCategories
    pass

def register():
    # if we use F8 reload this happens.
    if "ANIMATIONNODES" in nodeitems_utils._node_categories:
        unregister_node_categories("ANIMATIONNODES")
    
    #The First parameter is Like a id, that holds your nodeCategories registration, Later used to UnRegister
    register_node_categories("TRAFFICNODES", nodeCategories)
    if True:
        print("Traffic Nodes Menu was Made")
    
def unregister():
    unregister_node_categories("TRAFFICNODES")
    if True:
        print("Traffic Nodes Menu was Destroyed")
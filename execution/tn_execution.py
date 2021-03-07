import bpy

#CURRENT EXECUTION SYSTEM is ONLY BASED on tn.execute_node_tree.... 
#This is the way!
class ExecuteNodeTree(bpy.types.Operator):
    bl_idname = "tn.execute_node_tree"
    bl_label = "Execute Node Tree"
    
    nodeTreeName: bpy.props.StringProperty()
            
    def execute(self, context):
        nodeTree = bpy.data.node_groups.get(self.nodeTreeName)
        if nodeTree is None: return {'FINISHED'}
        
        TrafficNodeTree = ExecTrafficNodeTree(nodeTree)
        TrafficNodeTree.execute()
        
        return {'FINISHED'}


# EXECUTION HELPERS
# ---------------------
class ExecTrafficNodeTree:
    def __init__(self, nodeTree):
        self.nodeTree = nodeTree
        self.nodes = {}
        for node in nodeTree.nodes:
            self.nodes[node.name] = ExecTrafficNode(node)
    
    def execute(self):
        for node in self.nodes.values():
            node.isUpdated = False
            
        for node in self.nodes.values():
            if not node.isUpdated:
                self.updateNode(node)
        
    def updateNode(self, node):
        dependencyNames = node.getDependencyNodeNames()
        for name in dependencyNames:
            if not self.nodes[name].isUpdated:
                self.updateNode(self.nodes[name])
        self.generateInputList(node)
        node.execute()
        node.isUpdated = True
        
    def generateInputList(self, node):
        node.input = {}
        
        #do node.node because first node refers to ExecTrafficNode Type
        for socket in node.node.inputs:
            value = None
            if socket.is_linked:
                parentNode = self.nodes[socket.links[0].from_node.name]
                
                #this is the output variable of ExecTrafficNode
                value = parentNode.output[socket.links[0].from_socket.name]
            else:
                value = socket.getValue()
                
            node.input[socket.name] = value



class ExecTrafficNode:
    def __init__(self, node):
        self.node = node
        self.isUpdated = False
        
        #Dictionaries, Either Points to another Socket [if linked], or contains Value like STR, INT, FLT
        self.input = {}
        self.output = {}
        
    def getDependencyNodeNames(self):
        node = self.node
        dependencies = []
        for input in node.inputs:
            # TODO: check for reroute nodes
            # TODO: input.links takes more time, Optimize it, maybe cache it in an array inside every node
            if input.is_linked: dependencies.append(input.links[0].from_node.name)
        return dependencies
    
    def execute(self):
        self.output = self.node.execute(self.input)

# ---------------------
# EXECUTION HELPERS
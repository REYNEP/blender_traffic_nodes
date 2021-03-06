import bpy

def getActive():
    return bpy.context.active_object

def getNode(treeName, nodeName):
    return bpy.data.node_groups[treeName].nodes[nodeName]

def getTrafficNodeTree(context):
    return context.space_data.node_tree
import bpy
from . tn_ui_utils import *
from .. tn_utils import *


#This is a set, Don't Misjudge for Dictionary
classesNotToReg = {
    'SetupNodeTree'
}


class TN_PT_TrafficNodesPanel(bpy.types.Panel):
    bl_idname = "TN_PT_traffic_nodes_panel"
    bl_label = "Traffic Nodes"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Tool"
    bl_context = "objectmode"
    
    @classmethod
    def poll(self, context):
        area = context.space_data
        isNodeEditor = (area.type == 'NODE_EDITOR')
        if isNodeEditor and hasattr(area.node_tree, 'isTrafficNodeTree'):
            return area.node_tree.isTrafficNodeTree
        else:
            return False
    
    def draw(self, context):
        layout = self.layout
        nodeTree = getTrafficNodeTree(context).name

        #setup = layout.operator("tn.setup_node_tree")
        #setup.nodeTreeName = nodeTree

        layout.separator()
        execute = layout.operator("tn.execute_node_tree")
        execute.nodeTreeName = nodeTree


class SetupNodeTree(bpy.types.Operator):
    bl_idname = "tn.setup_node_tree"
    bl_label = "Create Node Tree Essentials"

    nodeTreeName: bpy.props.StringProperty()

    def execute(self, context):
        return self.manualExec(context)
    
    def invoke(self, context, event):
        return self.manualExec(context, event)
        
    def manualExec(self, context, event = None):
        nodeTree = bpy.data.node_groups.get(self.nodeTreeName)
        if nodeTree is None: return {'FINISHED'}
        
        AddNodesAtCenter(["ViewerNode"], nodeTree, 0)
        
        if event:
            bpy.ops.node.translate_attach_remove_on_cancel('INVOKE_DEFAULT')
        
        return {'FINISHED'}
from bpy.utils import register_class, unregister_class
from bpy.types import NodeTree
from bpy.props import BoolProperty

class TrafficNode: 
    @classmethod
    def poll(cls, nodeTree):
        return nodeTree == "TrafficNodeTreeType"

class TrafficNodesTree(NodeTree):
    """Trafic Nodes Editor"""
    bl_idname = "TrafficNodeTreeType"
    bl_label = 'Traffic Nodes'
    bl_icon = 'GRID'
    
    isTrafficNodeTree: BoolProperty(default = True)

    def update(self):
        #Did some tests, Feels like, this is only invoked, when A New Node is added or a Socket is Changed
        pass
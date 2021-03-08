from bpy.utils import register_class, unregister_class
from bpy.types import NodeTree, Object, Collection
from bpy.props import BoolProperty, PointerProperty
import bpy

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
        #TODO
        pass

#TODO INSPECT MAYBE SEP into another file 
class ObjectPropertyGroup(bpy.types.PropertyGroup):
    object: PointerProperty(type = Object)
    
class CollectionPropertyGroup(bpy.types.PropertyGroup):
    collection: PointerProperty(type = Collection)
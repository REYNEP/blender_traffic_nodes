import bpy
import os
import numpy as np
from pathlib import Path
from bpy.utils import register_class, unregister_class
# TODO MAYBE OPTIMIZE
from .. tn_utils import *

class AssignActiveObjectToNode(bpy.types.Operator):
    """Button that assigns your current active object to this NodeSocket"""
    bl_idname = "tn.assign_active_object_to_node"
    bl_label = "Assign Active Object"
    
    nodeTreeName: bpy.props.StringProperty()
    nodeName: bpy.props.StringProperty()
    target: bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return getActive() is not None
    
    def execute(self, context):
        obj = getActive()
        node = getNode(self.nodeTreeName, self.nodeName)
        #INSPECT
        setattr(node, self.target, obj)
        return {'FINISHED'}
    
class NewPropertyToListNode(bpy.types.Operator):
    bl_idname = "tn.new_property_to_list_node"
    bl_label = "New Object Pointer Property To Pointer List Node"
    
    nodeTreeName: bpy.props.StringProperty()
    nodeName: bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return getActive() is not None
    
    def execute(self, context):
        node = getNode(self.nodeTreeName, self.nodeName)
        node.addItemCP()
        return {'FINISHED'}
    
class NewCollectionToListNode(bpy.types.Operator):
    bl_idname = "tn.new_collection_to_list_node"
    bl_label = "New Collection Pointer Property To Object List Node"
    
    nodeTreeName: bpy.props.StringProperty()
    nodeName: bpy.props.StringProperty()
    
    @classmethod
    def poll(cls, context):
        return getActive() is not None
    
    def execute(self, context):
        node = getNode(self.nodeTreeName, self.nodeName)
        node.addCCP()
        return {'FINISHED'}
    
class RemoveCollectionFromListNode(bpy.types.Operator):
    bl_idname = "tn.remove_collection_from_list_node"
    bl_label = "Remove Collection Pointer Property from Object List Node"
    
    nodeTreeName: bpy.props.StringProperty()
    nodeName: bpy.props.StringProperty()
    index: bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        return getActive() is not None
        
    def execute(self, context):
        node = getNode(self.nodeTreeName, self.nodeName)
        node.removeCCP(self.index)
        return {'FINISHED'}
    
class RemovePropertyFromListNode(bpy.types.Operator):
    bl_idname = "tn.remove_property_from_list_node"
    bl_label = "Remove Object Property from String List Node"
    
    nodeTreeName: bpy.props.StringProperty()
    nodeName: bpy.props.StringProperty()
    index: bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        return getActive() is not None
        
    def execute(self, context):
        node = getNode(self.nodeTreeName, self.nodeName)
        node.removeItemCP(self.index)
        return {'FINISHED'}
    
class AssignActiveObjectToListNode(bpy.types.Operator):
    bl_idname = "tn.assign_active_object_to_list_node"
    bl_label = "Assign Active Object"
    
    nodeTreeName: bpy.props.StringProperty()
    nodeName: bpy.props.StringProperty()
    index: bpy.props.IntProperty()
    
    @classmethod
    def poll(cls, context):
        return getActive() is not None
        
    def execute(self, context):
        obj = getActive()
        node = getNode(self.nodeTreeName, self.nodeName)
        node.setObject(obj, self.index)
        return {'FINISHED'}
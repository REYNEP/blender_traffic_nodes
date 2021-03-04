'''
Copyright (C) 2021 REYNEP
parkeramitrakshar@gmail.com

Created by REYNEP
Thanks to JaquesLucke [Creator of Animation Nodes and Geo Nodes in Blender], 
Because of the Inspiration and also I mostly Followed His Older Code to Do it Faster [Meaning that, Yes I did copy Parts of His code from 2014-2015]

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import bpy
from bpy.utils import register_class, unregister_class
# TODO MAYBE OPTIMIZE
from tn_utils import *

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



# Register
# -------------
nopsClasses = [
	AssignActiveObjectToNode,
	NewPropertyToListNode,
	RemovePropertyFromListNode,
	NewCollectionToListNode,
	RemoveCollectionFromListNode,
	AssignActiveObjectToListNode,
]

def register():
	for cls in nopsClasses:
		register_class(cls)
		if True:
			print(cls, " Registered")

def unregister():
	for cls in nopsClasses:
		unregister_class(cls)
		if True:
			print(cls, " Registered")
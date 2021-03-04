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
#TODO INSPECT
from tn_utils import *

class TN_PT_TrafficNodesPanel(bpy.types.Panel):
	bl_idname = "TN_PT_traffic_nodes_panel"
	bl_label = "Traffic Nodes"
	bl_space_type = "NODE_EDITOR"
	bl_region_type = "UI"
	bl_category = "Tool"
	bl_context = "objectmode"
	
	@classmethod
	def poll(self, context):
		area = context.area.spaces.active
		isNodeEditor = (area.type == 'NODE_EDITOR')
		if isNodeEditor and hasattr(area.node_tree, 'isTrafficNodeTree'):
			return area.node_tree.isTrafficNodeTree
		else:
			return False
	
	def draw(self, context):
		layout = self.layout
		execute = layout.operator("tn.execute_node_tree")
		execute.nodeTreeName = getTrafficNodeTree(context).name

class ExecuteNodeTree(bpy.types.Operator):
	bl_idname = "tn.execute_node_tree"
	bl_label = "Execute Node Tree"
	
	nodeTreeName = bpy.props.StringProperty()
			
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



# Register
# -------------

def register():
	bpy.utils.register_class(TN_PT_TrafficNodesPanel)
	bpy.utils.register_class(ExecuteNodeTree)
	if True:
		print("TN_PT_TrafficNodesPanel Registered")
		print("ExecuteNodeTree Registered")

def unregister():
	bpy.utils.unregister_class(TN_PT_TrafficNodesPanel)
	bpy.utils.unregister_class(ExecuteNodeTree)
	if True:
		print("TN_PT_TrafficNodesPanel UnRegistered")
		print("ExecuteNodeTree UnRegistered")
'''
Copyright (C) 2021 REYNEP
parkeramitrakshar@gmail.com

Created by REYNEP
Thanks to JaquesLucke [Creator of Animation Nodes and Geo Nodes in Blender], 
Because of the Inspiration and also I mostly Followed His Older Code to Do it Faster [Meaning that, Yes I did copy Parts of His code]

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
	#The First parameter is Like a id, that holds your nodeCategories registration, Later used to UnRegister
	register_node_categories("TRAFFICNODES", nodeCategories)
	if True:
		print("Traffic Nodes Menu was Made")
	
def unregister():
	unregister_node_categories("TRAFFICNODES")
	if True:
		print("Traffic Nodes Menu was Destroyed")
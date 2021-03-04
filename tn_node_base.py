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
		#TODO
		pass

def register():
	register_class(TrafficNodesTree)
	if True:
		print("TrafficNodesTree Registered")

def unregister():
	unregister_class(TrafficNodesTree)
	if True:
		print("TrafficNodesTree UnRegistered")
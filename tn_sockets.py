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
from bpy.types import NodeSocket
from bpy.props import StringProperty

class GenericSocket(NodeSocket):
	bl_idname = "GenericSocket"
	bl_label = "Generic Socket"
	
	def draw(self, context, layout, node, text):
		layout.label(text = text)
	def draw_color(self, context, node):
		return (0.5, 0, 0, 0.8)
	
	def getValue():
		return "NO INPUT"

class ObjectSocket(NodeSocket):
	bl_idname = "ObjectSocket"
	bl_label = "Object Socket"
	
	objectName: StringProperty()
	
	def draw(self, context, layout, node, text):
		if not self.is_output and not self.is_linked:
			col = layout.column()
			row = col.row(align = True)
			row.prop(self, "objectName", text = "")
			selector = row.operator("tn.assign_active_object_to_socket", text = "", icon = "EYEDROPPER")
			selector.nodeTreeName = node.id_data.name
			selector.nodeName = node.name
			selector.isOutput = self.is_output
			selector.socketName = self.name
			selector.target = "objectName"
			col.separator()
		else:
			txt = text
			layout.label(text=txt)
			
	def draw_color(self, context, node):
		return (0, 0, 0, 1)

	def getValue(self):
		return self.objectName
	
class ObjectListSocket(NodeSocket):
	bl_idname = "ObjectListSocket"
	bl_label = "Object List Socket"
	
	def draw(self, context, layout, node, text):
		layout.label(text = text)
	def draw_color(self, context, node):
		return (0, 0, 0, 0.5)
	
	def getValue(self):
		return "No Object List Input"


# Register
# -------------
def register():
	register_class(GenericSocket)
	register_class(ObjectSocket)
	register_class(ObjectListSocket)
	if True:
		print("GenericSocket Registered")
		print("ObjectSocket Registered")
		print("ObjectListSocket Registered")

def unregister():
	unregister_class(GenericSocket)
	unregister_class(ObjectSocket)
	unregister_class(ObjectListSocket)
	if True:
		print("GenericSocket UnRegistered")
		print("ObjectSocket UnRegistered")
		print("ObjectListSocket UnRegistered")
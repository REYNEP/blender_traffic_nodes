from bpy.utils import register_class, unregister_class
from bpy.types import NodeSocket
from bpy.props import StringProperty, FloatVectorProperty


classesNotToReg = {
    'Vec3DListSocket',
    'Vec3DSocket'
}

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
            layout.label(text = text)
            
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

class Vec3DSocket(NodeSocket):
    bl_idname = "Vec3DSocket"
    bl_label = "Vec3D Socket"
    
    #Precision is Display Precision, Default value is 0.0, 0.0., 0.0
    #TODO: INSPECT Docs on this
    vec3D: FloatVectorProperty(precision = 2, size = 3)
    
    #TODO: INSPECT This doesn't Seem important
    def draw(self, context, layout, node, text):
        layout.label(text = text)
            
    def draw_color(self, context, node):
        return (0.15, 0.15, 0.8, 1.0)

    def getValue(self):
        return self.vec3D
    
class Vec3DListSocket(NodeSocket):
    bl_idname = "Vec3DListSocket"
    bl_label = "Vec3D List Socket"
    
    def draw(self, context, layout, node, text):
        layout.label(text = text)

    def draw_color(self, context, node):
        return (0.15, 0.15, 0.8, 0.5)
    
    def getValue(self):
        return "No Object List Input"
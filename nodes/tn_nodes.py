# TODO: Maybe Emit the next Line, See Line #32, #126
import os
import array
import time

import bpy
from bpy.types import Node, Object, Collection, Text
from bpy.props import PointerProperty, CollectionProperty, BoolProperty, FloatVectorProperty
# Lets See if this FIxes the issue or not
from . tn_node_base import TrafficNode



#TODO INSPECT MAYBE SEP into another file 
class ObjectPropertyGroup(bpy.types.PropertyGroup):
    object: PointerProperty(type = Object)
    
class CollectionPropertyGroup(bpy.types.PropertyGroup):
    collection: PointerProperty(type = Collection)

class ViewerNode(Node, TrafficNode):
    bl_idname = "ViewerNode"
    bl_label = "Viewer Node Mk.1"
    
    textBlock: PointerProperty(type = Text)
    #INSPECT for Maybe making this a simple boolean
    #is_socketLinked: bpy.props.BoolProperty(default = False)
    
    def init(self, context):
        self.inputs.new("GenericSocket", "Data")
        
    def draw_buttons(self, context, layout):
        col = layout.column(align = True)
        row = col.row(align = True)
        row.prop(self, "textBlock", text = "TextBlock")
            
    def execute(self, input):
        if self.inputs["Data"].is_linked:
            if self.textBlock is not None:
                self.textBlock.clear()
                text = str(input)
                self.textBlock.write(text)



class ObjectListToLocationsList(Node, TrafficNode):
    bl_idname = "ObjectListToLocationsList"
    bl_label = "Object List To Locations List"

    locationCP = []

    def init(self, context):
        self.inputs.new("ObjectListSocket", "Object List")
        self.outputs.new("Vec3DListSocket", "Location List")

    def execute(self, input):
        output = {}

        index = 0
        for obj in input['Object List']:
            self.locationCP.append(obj.location)
            index += 1

        output["Location List"] = self.locationCP
        return output

class SetInitialPositionsNode(Node, TrafficNode):
    bl_idname = "SetInitialPositionsNode"
    bl_label = "Set Initial Pos Mk.1"

    isCacheDir = False
    blenDir = ''
    cacheDir = ''
    cacheDirRelative = 'TNCache'

    def init(self, context):
        self.inputs.new("Vec3DListSocket", "Location List")

    def execute(self, input):
        if not self.checkCacheDir():
            bpy.ops.error.message('INVOKE_DEFAULT', type = "Error", message = 'You have to Save Blender For Now')
            return
        else:
            print(time.time())
            locVec3DList = input["Location List"]
            flattened = []
            for vec3D in locVec3DList:
                for axis in vec3D:
                    flattened.append(axis)
            print(time.time())

            pos = array.array('d', flattened)
            binFile = open(os.path.join(self.cacheDirRelative, 'init_pos.bin'), 'wb')

            print(time.time())
            pos.tofile(binFile)
            print(time.time())

            binFile.close()

    def checkCacheDir(self):
        if bpy.data.is_saved:
            self.blenDir = os.path.dirname(bpy.data.filepath)
            self.cacheDir = os.path.join(self.blenDir, "TNCache")
            self.isCacheDir = os.path.exists(self.cacheDir)

            if not self.isCacheDir:
                os.mkdir(self.cacheDir)
                self.isCacheDir = True

            return True
        else:
            return False
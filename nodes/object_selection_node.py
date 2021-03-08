from bpy.types import Node, Object
from bpy.props import PointerProperty, CollectionProperty, BoolProperty

from . tn_node_base import TrafficNode
from . tn_nodes import ObjectPropertyGroup, CollectionPropertyGroup

class ObjectSelectionNode(Node, TrafficNode):
    bl_idname = "ObjectSelectionNode"
    bl_label = "Objects Selection Mk.1"
    
    object: PointerProperty(type = Object)
    
    objectCP: CollectionProperty(type = ObjectPropertyGroup)
    collectionCP: CollectionProperty(type = CollectionPropertyGroup)
    showEditOptions: BoolProperty(default = False)
    
    def init(self, context):
        self.outputs.new("ObjectSocket", "Object")
        self.outputs.new("ObjectListSocket", "Object List")
        
    def draw_buttons(self, context, layout):
        # SINGLE OBJECT INPUT AREA
        col = layout.column(align = True)
        row = col.row(align = True)
        row.prop(self, "object", text = "")
        selector = row.operator("tn.assign_active_object_to_node", icon = "EYEDROPPER", text = "")
        selector.nodeTreeName = self.id_data.name
        selector.nodeName = self.name
        selector.target = "object"
        col.separator()
        
        # OBJECT LIST INPUT AREA
        col.separator()
        col.separator()
        row = col.row(align = True)
        row.scale_y = 1
        listBelow = row.label(text = "GenObjList [Excl.Above1]")
        row.prop(self, "showEditOptions", text = "Show Options")
        
        indexOBJ = 0
        indexCOL = 0
        if self.showEditOptions:
            for item in self.objectCP:
                row = col.row(align = True)
                row.scale_y = 1
                select = row.operator("tn.assign_active_object_to_list_node", icon = "EYEDROPPER", text="")
                select.nodeTreeName = self.id_data.name
                select.nodeName = self.name
                select.index = indexOBJ
                row.prop(item, "object", text = "")
                remove = row.operator("tn.remove_property_from_list_node", text = "", icon = "X")
                remove.nodeTreeName = self.id_data.name
                remove.nodeName = self.name
                remove.index = indexOBJ
                indexOBJ += 1
            col.separator()
            add = col.operator("tn.new_property_to_list_node", text = "New Object", icon = "PLUS")
            add.nodeTreeName = self.id_data.name
            add.nodeName = self.name
            
            #COLLECTION INPUT AREA
            col.separator()
            for item in self.collectionCP:
                row = col.row(align = True)
                row.scale_y = 1
                row.prop(item, "collection", text = "")
                remove = row.operator("tn.remove_collection_from_list_node", text = "", icon = "X")
                remove.nodeTreeName = self.id_data.name
                remove.nodeName = self.name
                remove.index = indexCOL
                indexCOL += 1
            col.separator()
            add2 = col.operator("tn.new_collection_to_list_node", text = "New Collection", icon = "PLUS")
            add2.nodeTreeName = self.id_data.name
            add2.nodeName = self.name
            col.separator()
        
    def execute(self, input):
        output = {}
        output["Object List"] = self.getCurrentList()

        #TODO Improve this. Improvise this... Currently the logic sucks
        if self.object is not None:
            output["Object"] = bpy.data.objects.get(self.object.name)
        else:
            output["Object"] = "No SINGLE Object selected"
        return output
        
    def getCurrentList(self):
        objectList = []
        
        for item in self.objectCP:
            objectList.append(item.object)
            
        for C in self.collectionCP:
            for obj in C.collection.objects:
                objectList.append(obj)
                
        return objectList
        
    def addItemCP(self):
        item = self.objectCP.add()
        
    def removeItemCP(self, index):
        self.objectCP.remove(index)
        
    def setObject(self, object, index):
        self.objectCP[index].object = object
        
    def addCCP(self):
        item = self.collectionCP.add()
        
    def removeCCP(self, index):
        self.collectionCP.remove(index)
    
    def setCollection(self, object, index):
        self.collectionCP[index].object = object
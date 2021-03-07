"""This Module Loads all the Other modules, Calls Register() functions if those modules have any, Thus Registering modules that can be reg. to Blender"""

#Req for loadModules
import pkgutil
from pathlib import Path
import importlib
#Req for loadClasses
import bpy.types
import inspect
import typing

import bpy.utils



moduleNames = []
modulesImported = []
moduleClasses = []
dependencyClasses = []      #Note that dependencyClasses are also inside MODULES which were Imported

# LIBRARY UTILITIES
# [a.k.a Functions that are used by the LIBRARY FUNCTIONS, (See Below for LIBRARY FUNCS)]
# If you want Docs, 3Below ;)
# --------------------------##############################--------------------------------
# [The 2 Functions Below, Should not be called outside of loadModules]
def getModuleNames(root, package = ''):
    """Creates a Generator Object which later can be used to importModules. Generates ModuleNames absolute to AddonDirectory. 
    All py files inside your addon dir and Addon Packages are Modules. Package is explaine in the Next Comment 6 lines after this line
    """
    if not isinstance(root, Path):
        root = Path(root)
    
    absolutePath = package
    for moduleDir, moduleName, ispkg in pkgutil.iter_modules([str(root)]):
        #A Package is simply a Directory which has a __init__.py inside it, So yes if you have py files inside a Dir which need to be reg. make __init__.py
        if ispkg:
            rootNext = root / moduleName
            absolutePathNext = absolutePath + moduleName + '.'

            print("Found A Package:- ", moduleName)

            yield from getModuleNames(rootNext, absolutePathNext)
        else:
            print("Found A Module:- ", moduleName)
            yield absolutePath + moduleName


def importModules(addonDirName):
    return [importlib.import_module('.' + moduleName, addonDirName) for moduleName in moduleNames if moduleName != __name__]

    #I used a list comprenhension because it's almost 50% faster https://stackoverflow.com/q/30245397
    #similar to this Below
    #for tnModuleName in tnModuleNames:
    #    normally getModuleNames yields/returns this load_and_reg file too, so we check for that case
    #    if tnModuleName == __name__:
    #        continue
    #    else:
    #        importedModules.append(importlib.import_module('.' + tnModuleName, addonDirName))

def getSubClasses(parentClasses):
    """ return all the SubClasses which's parent Class is in parentClasses searching throught all the modulesImported"""
    classesToRegister = []

    for module in modulesImported:
        for value in module.__dict__.values():
            if inspect.isclass(value):
                #issubclass does support passing in a tuple or list
                if issubclass(value, parentClasses) and not hasattr(bpy.types, value.__name__):
                    print(value, "appending")
                    classesToRegister.append(value)

    return classesToRegister

def getDependencyClasses():
    dependencies = []

    alreadyAdded = []
    for cls in moduleClasses:
        #TO Understand what's Really going On here: https://www.youtube.com/watch?v=2wDvzy6Hgxg [Guido Introduces Type Hints, PyCon 2015]
        if not hasattr(cls, "__annotations__"):
            continue
        for value in typing.get_type_hints(cls, {}, {}).values():
            if isinstance(value, tuple) and len(value) == 2:
                if value[0] in (bpy.props.PointerProperty, bpy.props.CollectionProperty):
                    dependency = value[1]["type"]
                    if dependency not in alreadyAdded:
                        alreadyAdded.append(dependency)
                        if hasattr(bpy.types, dependency.__name__):
                            continue
                        dependencies.append(dependency)
    
    return dependencies




# WHAT YOU CAME HERE FOR 
# [a.k.a LIBRARY FUNCTIONS for PEOPLE WHO WANT TO AUTOMATE BLENDER ADDON REGISTRATION]
# --------------------------##############################--------------------------------

# RULES
# 1. if you have .py files inside some directories, you need to have __init__.py file inside those directories. [empty __init__.py is okay]
# 1.1 This Treats that directory as a Package
# 1.2 A Package is simply a Directory which has a __init__.py inside it, So yes if you have py files inside a Dir which need to be reg. make __init__.py
# --
# 2. call loadModules, parameter should be the directory that your addon is inside
# 3. You can call registerModules(), in that case all your modules which has register will be called, and you will need to manually do bpy.utils.register_class() inside those
# --
# 4. Or, you can call loadClasses, after loadModules, which will load all the classes which are subclasses of bpy.types.Type
# 4.1 if any of your Classes has a bpy.props.PointerProperty or bpy.props.CollectionProperty, [note that these 2 props has 'type' parameter] with type set to manual type
# ---- e.g. class CollectionPropertyGroup(bpy.types.PropertyGroup):
# ----           object: PointerProperty(type = Object)
# ----
# ---- then used like this, 
# ----       objectCP: CollectionProperty(type = ObjectPropertyGroup)
# ----
# ---- in that case ObjectPropertyGroup is considered to be a dependencyClass and is registered before all the other classes are registered
# 5. Call registerClasses() [THE END]

def loadModules(addonDir):
    global moduleNames
    global modulesImported

    #For Now moduleNames is just a Generator Object [Generator Objects:- https://www.youtube.com/watch?v=ixiRkUwPI2A&t=3700s]
    moduleNames = getModuleNames(addonDir)

    if not isinstance(addonDir, Path):
        addonDir = Path(addonDir)
    addonDirName = addonDir.name

    modulesImported = importModules(addonDirName)

#Use this when you have an register() function inside all your modules that need to be registered, meaning that use this when doing register_class inside every module itself
def registerModules():
    for module in modulesImported:
        if hasattr(module, 'register'):
            module.register()

def unregisterModules():
    for module in modulesImported:
        if hasattr(module, 'unregister'):
            module.unregister()




# You can Either Add any Type from bpy.types here inside bpyTypes, 
# Or you can make your own tuple/list like I did and pass that to loadClasses 
bpyTypesDefault = tuple(getattr(bpy.types, name) for name in [
    'Operator',
    'Panel',
    'PropertyGroup'
])

def loadClasses(parentClasses = bpyTypesDefault):
    """ Load all the Classes which are SubClasses of parentClasses, usually we need to bpy.utils.register_class() which have at least one bpy.types.{ClassName} as base"""
    global moduleClasses
    global dependencyClasses

    moduleClasses = getSubClasses(parentClasses)
    dependencyClasses = getDependencyClasses()

    for cls in dependencyClasses:
        moduleClasses.remove(cls)

def registerClasses():
    for cls in dependencyClasses:
        print("rEG DEP:-", str(cls))
        bpy.utils.register_class(cls)

    for cls in moduleClasses:
        print("rEG:-", str(cls))
        bpy.utils.register_class(cls)

def unregisterClasses():
    for cls in moduleClasses:
        print("uNrEG:-", str(cls))
        bpy.utils.unregister_class(cls)

    for cls in dependencyClasses:
        print("uNrEG:-", str(cls))
        bpy.utils.unregister_class(cls)















# EXTENDED VERSIONS, UNDER CONSTRUCTION, STAY AT A SAFE DISTANCE, SEE ABOVE FOR WHAT YOU CAME FOR
# --------------------------#################################-------------------------------------


# Extended Versions, [TODO]
# Older Implementations,
# Documentations - [TODO]
# As the Functions above are sorted, [Top-to-Bottom]
# --------------------------#################################-------------------------------------

""" getModuleNames(root, package = '')
This function Gets all modules inside of a directory
---------------------------------------------------------
Okay, So here's How you will have to Use it. 
You literally have to do nothing, All the *.py files will be yielded as a str, eg. tn_utils, nodes.tn_node_base, nodes.tn_nodes
where, tn_utils is .py file, 
       nodes is a subdirectory inside our root [See root param], 
       tn_node_base, tn_nodes are .py files inside nodes subdir
Remember, 
       it for now only yields the name of only .py files, 
       and not the Directories [a.k.a packages]
       meaning that it won't yield only 'nodes' unless you have third param to TRUE
Later, 
       you can use these strings with import, 
       you can do a "from . import nodes.tn_node_base" or such, 
       but if you don't want 'from .' to be used, you know You can just append the path to your addon to sys.path 
-----------------------------------------------------------------------------------------------------------------
Only remember that pkgutil.iter_modules will return moduleName for all .py files inside of that directory that you pass as param to it
It won't recognize any directory as a module [Yes in Python directories can be module, or more specifically the community calles them packages]
As I was saying, it won't recognize if your directory doesn't have an __init__.py inside of it, if you're wondering, __init__.py can be empty thought
-------------------------------------------------------
pkgutil.iter_modules performs almost 20x faster for me already, and I guess the highest can be like 50x when you have a really conplex project
*Faster than os.walk 
#iter_modules searches the path in alphabetical order
"""
# IMPLEMENTATION from 0.0.1 [Before 0.1a we had 0.0.1, 0.0.2 ... TODO Update last version number]
#def getModuleNamesBruteForce(root):
#	pattern = "*.py"
#	for root, subdirs, files in os.walk(root):
#		for file in files:
#			if fnmatch(file, pattern):
#				yield root + file

def getModuleNamesExt(root, package = '', depth = -1, yieldPkgs = False):
    """
    Let's Say that your all packages have an __init__.py inside each, and you just want those __init__.py to be yieled,
    I mean you just want those Packages to be imported then that Package might a Function and that Function could be responsible for importing other .py files inside the package
    That's where you set yieldPkgs, or [a.k.a dontYieldSubModules]
    ...
    And then comes
        the 4th param, depth by default is unlimited [a.k.a. -1],
        you can limit by at least passing 1, 
        0 or below will only cause errors
    if that is set to 1, it means, it will yield only the packages inside your ADDON's root directory 

    NOTE: This function is Under Construction!!! Stay at a Minimum Safety Distance
    """
    is_depthLimit = True
    if depth == 0: return
    elif depth == -1: is_depthLimit = False

    if not isinstance(root, Path):
        root = Path(root)

    absolutePath = package
    for moduleDir, moduleName, ispkg in pkgutil.iter_modules([str(root)]):
        #A Package is a 
        if ispkg:
            rootNext = root / moduleName
            absolutePathNext = absolutePath + moduleName + '.'
            
            print("Found A Package:- ", moduleName)

            if is_depthLimit: depthNext = depth - 1
            else: depthNext = -1
            yield from getModuleNames(rootNext, absolutePathNext, depthNext)
        else:
            print("Found A Module:- ", moduleName)
            yield absolutePath + moduleName
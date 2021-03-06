#This Module Loads all the Other modules, Calls Register() functions if those modules have any, Thus Registering modules that can be reg. to Blender
import pkgutil
from pathlib import Path
import importlib

#tnModuleNames are just strings, tnModulesImported refer to actual modules which are imported
tnModuleNames = []
tnModulesImported = []

#If you want Docs, 3Below ;)
def getModuleNames(root, package = ''):
    if not isinstance(root, Path):
        root = Path(root)
    
    absolutePath = package
    for moduleDir, moduleName, ispkg in pkgutil.iter_modules([str(root)]):
        #A Package is a 
        if ispkg:
            rootNext = root / moduleName
            absolutePathNext = absolutePath + moduleName + '.'

            print("Found A Package:- ", moduleName)

            yield from getModuleNames(rootNext, absolutePathNext)
        else:
            print("Found A Module:- ", moduleName)
            yield absolutePath + moduleName


def importModules(addonDirName):
    #normally getModuleNames yields/returns this load_and_reg file too, so we manually remove that, so that we don't have to check tnModule == __name__ ever again
    #Then we Import the other Modules
    for tnModuleName in tnModuleNames:
        if tnModuleName == __name__:
            tnModuleNames.remove(tnModuleName)
            continue
        else:
            yield importlib.import_module('.' + tnModuleName, addonDirName)

#Consists of two steps, Loading the names of the modules in tnModuleNames, STEP 2 is to import the Modules
def loadModules(addonDir):
    global tnModuleNames
    global tnModulesImported

    tnModuleNames = getModuleNames(addonDir)

    if not isinstance(addonDir, Path):
        addonDir = Path(addonDir)
    addonDirName = addonDir.name

    tnModulesImported = importModules(addonDirName)

def registerModules():
    for tnModule in tnModulesImported:
        if hasattr(tnModule, 'register'):
            tnModule.register()

def unregisterModules():
    for tnModule in tnModulesImported:
        if hasattr(tnModule, 'unregister'):
            tnModule.unregister()



# Extended Versions, [TODO]
# Older Implementations,
# Documentations - [TODO]
# As the Functions above are sorted, [Top-to-Bottom]
# ------------------------------------------------------------------------

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
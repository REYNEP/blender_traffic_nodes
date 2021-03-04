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
import bpy, sys, os
from fnmatch import fnmatch

bl_info = {
	"name":         "Traffic Nodes",
	"description":  "Node system for more flexible Traffic System Simulation",
	"author":       "REYNEP",
	"version":      (0, 0, 1),
	"blender":      (2, 93, 0),
	"location":     "Node Editor",
	"category":     "Animation",
	"warning":	    "alpha",
	"doc_url":      "TO BE ADDED SOON",
	"tracker_url":  "Feel Free to mail me for Now",
}


# import all modules in same/subdirectories
# ------------------------------------------
currentPath = os.path.dirname(__file__)

def getAllPathsToPythonFiles(root):
	filePaths = []
	pattern = "*.py"
	dirPaths = []

	# every folder can have multiple files or subDirectories, os.walk simply walks into every directory, [new iteration means new directory]
	for (path, subDirectories, files) in os.walk(root):
		foundPYinDIR = False
		for name in files:
			if fnmatch(name, pattern): 
				foundPYinDIR = True
				filePaths.append(os.path.join(path, name))
		if foundPYinDIR:
			dirPaths.append(path)

	return [filePaths, dirPaths]

#We could have merged this one into the Above one, But what's the Point. WE are Making Nodes Today Anyway
def getModuleNames(filePaths):
	moduleNames = []
	for filePath in filePaths:
		#splitext splits into PAIR of (root, ext), so we take root with '[0]'
		moduleName = os.path.basename(os.path.splitext(filePath)[0])
		if moduleName != "__init__":
			moduleNames.append(moduleName)
	return moduleNames


#Generate filePaths, dirPaths, moduleNames 
pyFilePaths, pyDirPaths = getAllPathsToPythonFiles(currentPath)
moduleNames = getModuleNames(pyFilePaths)

# Because we Still need to Import Those to Call those Functions
for dirPath in pyDirPaths:
	sys.path.append(dirPath)

for name in moduleNames:
	# TODO Maybe Import Only the Register() Function
	exec("import " + name)
	print("import " + name)

# END
# import all modules in same/subdirectories
# ------------------------------------------

# Register
# -----------

def registerIfPossible(moduleName):
	exec("global module; module = " + moduleName)
	if hasattr(module, "register"):
		module.register()
		
def unregisterIfPossible(moduleName):
	exec("global module; module = " + moduleName)
	if hasattr(module, "unregister"):
		module.unregister()


#No Need for   if __name__ == __main__, Blender calls register() by default when someone Enables the Addon
def register():
	for moduleName in moduleNames:
		registerIfPossible(moduleName)

	print("All TrafficNodes Modules Registered")

def unregister():
	for moduleName in moduleNames:
		unregisterIfPossible(moduleName)
	print("All TrafficNodes Modules UnRegistered")
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
# <pep8 compliant>

bl_info = {
    "name":         "Traffic Nodes",
    "description":  "Node system for more flexible Traffic System Simulation",
    "author":       "REYNEP",
    "version":      (0, 0, 1),
    "blender":      (2, 93, 0),
    "location":     "Node Editor",
    "category":     "Animation",
    "warning":	    "alpha",
    #"doc_url":      "TO BE ADDED SOON",
    #"tracker_url":  "Feel Free to mail me for Now",
}


import bpy
import os
import sys
from . import load_and_reg

# Load Modules, Then Call Register from each if Possible
# -----------------------------
currentDir = os.path.dirname(os.path.abspath(__file__))
load_and_reg.loadModules(currentDir)

# REGISTER, The Entire Addon
# -----------------------------
def register():
    load_and_reg.registerModules()
    print("Registered Traffic Nodes")
    
def unregister():
    load_and_reg.unregisterModules()
    print("UnRegistered Animation Nodes")
#No Need for   if __name__ == __main__, Blender calls register() by default when someone Enables the Addon
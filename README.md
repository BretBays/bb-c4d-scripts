# bb-c4d-scripts
A repository of a variety of python scripts for Cinema 4D.

# Installation
Download any and all files from the repository. Open up your copy of Cinema 4D and choose **Edit>Preferences**. At the bottom click the **Open Preferences Folder** button. From there, go into **library/scripts** and drop the files/folders into there. 

# Overview

## ANIMATION SCRIPTS
**DeleteAllAnimation.py/DeleteSelectedAnimation**: Quick script that lets you either kill all the animation within your scene, or just selected objects. Useful when rig testing.

**BB_Ghost**: Inspired by Brian Horgan's bh_ghost script for Maya, this script will take whatever polygonal objects you have selected and create 'Ghost' images for the current frame to help with your animation. It will overwrite existing ghosts if they already exist on this frame

## VERTEX MAP SCRIPTS
**ConvertJointtoVMap** Converts a joint's weights into a vertex map

**ConvertVmapToJoint** Converts a Vertex Map's weights to a joint

**VertexMap Import/Export** Import and export your vertex maps to a file on disk. Will re-create the maps on import. 

**InvertVertexMap** Will import your selected vertex map. If you have components selected, only those components will be inverted

## UTILITY SCRIPTS
**ExtrudeEmAll**: Select all your splines, and it will put them all in an ExtrudeNURBS and turn on Hierarchical for you

**GroupEach**: Takes your selected objects and puts each one under it's own null object and keeps it in the same location

**ParentToLastSelected**:Recreates Maya P key functionality for parenting objects by saying This object(s) should go under the last selected object. 

## WEIGHT SCRIPTS

**Increase/DecreaseWeightStrength**: Change the strength of the weights manager, weights brush, and paint brush(for vertex maps) by either 1, 5, or 10% depending on which keyboard modifiers you use. No modifier = 10%, CTRL = 5%, CTRL+SHIFT = 1% increments.




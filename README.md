# bb-c4d-scripts
A repository of a variety of python scripts for Cinema 4D.

# Installation
Download any and all files from the repository. Open up your copy of Cinema 4D and choose **Edit>Preferences**. At the bottom click the **Open Preferences Folder** button. From there, go into **library/scripts** and drop the files/folders into there. 

# Overview

## ANIMATION SCRIPTS
**[DeleteAllAnimation.py](https://www.dropbox.com/scl/fi/1bdjzbscanbpq8r6tc20d/DeleteAllAnim.mp4?rlkey=u86m30bmzgjqequ1eapf6dpju&dl=0)/[DeleteSelectedAnimation](https://www.dropbox.com/scl/fi/el5cxyohmg12voa2ec7v8/DeleteSelAnim.mp4?rlkey=to6srdwhc51ffcgu034bjb2bp&dl=0)**: Quick script that lets you either kill all the animation within your scene, or just selected objects. Useful when rig testing.

**[BB_Ghost](https://www.dropbox.com/scl/fi/46rxv3ap5juike78v1tvp/bb_ghost.mp4?rlkey=d8la9iczwp5cbn0qrbufszig8&dl=0)**: Inspired by Brian Horgan's bh_ghost script for Maya, this script will take whatever polygonal objects you have selected and create 'Ghost' images for the current frame to help with your animation. It will overwrite existing ghosts if they already exist on this frame

## VERTEX MAP SCRIPTS
**[ConvertJointtoVMap](https://www.dropbox.com/scl/fi/cliarvk3fx9wazpib87ak/jointToVMap.mp4?rlkey=3fdnn414o3h7sgtccj96exftr&dl=0)** Converts a joint's weights into a vertex map

**[ConvertVmapToJoint](https://www.dropbox.com/scl/fi/xkndon49xn92i2k26sotf/VMapToJoint.mp4?rlkey=utv1qld8ha7touox8xy95bksl&dl=0)** Converts a Vertex Map's weights to a joint

**[VertexMap Import/Export](https://www.dropbox.com/scl/fi/02buqfl3bs2uutkv2u2n5/ImportExportVmaps.mp4?rlkey=r9l61o83dgt4g6kuusla6bkm0&dl=0)** Import and export your vertex maps to a file on disk. Will re-create the maps on import. 

**[InvertVertexMap](https://www.dropbox.com/scl/fi/yjbnokk1ve93537yasa8h/InvertVMap.mp4?rlkey=0z1idocnyzaofk8hwm7tb1i9l&dl=0)** Will import your selected vertex map. If you have components selected, only those components will be inverted

**NormalizeVertexMap** Select your mesh, select 2 tags, and it will normalize any weights whos combined value is more than 100% will be normalized.

## UTILITY SCRIPTS
**[ExtrudeEmAll](https://www.dropbox.com/scl/fi/ia6gyc88k5f0c6rqt5va1/ExtrudeEmAll.mp4?rlkey=rnpeoq5mxgwip2fa1trhuifay&dl=0)**: Select all your splines, and it will put them all in an ExtrudeNURBS and turn on Hierarchical for you

**[GroupEach](https://www.dropbox.com/scl/fi/ejsowy5px6puwpqo2n9g4/GroupEach.mp4?rlkey=jb4sv1zovufi7muyjh7h2rpfr&dl=0)**: Takes your selected objects and puts each one under it's own null object and keeps it in the same location

**[ParentToLastSelected](https://www.dropbox.com/scl/fi/nbmbf3yztagwj5o80vcar/ParentToLast.mp4?rlkey=wnrl3a1hgcr6lz2aamkt7689r&dl=0)**:Recreates Maya P key functionality for parenting objects by saying This object(s) should go under the last selected object. 

## WEIGHT SCRIPTS

**[Increase/DecreaseWeightStrength](https://www.dropbox.com/scl/fi/c9ghx6wn82qvsnbuh4xtc/StrengthScripts.mp4?rlkey=s2ttve0vioffc3vzn1peqbca9&dl=0)**: Change the strength of the weights manager, weights brush, and paint brush(for vertex maps) by either 1, 5, or 10% depending on which keyboard modifiers you use. No modifier = 10%, CTRL = 5%, CTRL+SHIFT = 1% increments.




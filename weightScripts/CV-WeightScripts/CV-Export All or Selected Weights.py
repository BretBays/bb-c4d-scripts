"""
Name-US: CV-Export All or Selected Weights...
Description-US: Export all weight tags or only the selected weight tags to a specified directory
"""

import c4d
import os
from c4d import gui
#Welcome to the world of Python

def writeHeader():
    return "#CINEMA 4D Joint Weights File, written by CV Joint Weights Export\n"

def writeJoints(doc, tag):
    # Loop through all joints in the weight tag
    # and write the deformer index line:
    # deformer <index> <name>
    out = ""
    for j in range(0, tag.GetJointCount()):
        joint = tag.GetJoint(j, doc)
        if joint is not None:
            out = out + "\ndeformer " + str(j)
            out = out + " " + joint.GetName()
    return out+"\n"

def writeWeights(op, tag):
    # Write weight values
    out = ""
    for p in range(0, op.GetPointCount()):

        out = out + "\n" + str(p) + ":"
        # Loop through joints, and write ONLY joints with weight
        for j in range(0, tag.GetJointCount()):
            weight = tag.GetWeight(j, p)

            if weight > 0.0:
                out = out + " " + str(j) + " " + str(weight)
    return out

def GetAllPolygonObjects(obj, listy):
    if obj is None: return
    #Actions can go here
    if obj.GetType()==c4d.Opolygon:
        listy.append(obj)
    #End Actions
    if (obj.GetDown()):
        GetAllPolygonObjects(obj.GetDown(), listy)
    if (obj.GetNext()):
        GetAllPolygonObjects(obj.GetNext(), listy)

    return listy

def main():
    #Get all the polygon objects...
    polyObjs=doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
    if len(polyObjs)<=0:
        polyObjs=GetAllPolygonObjects(doc.GetFirstObject(), polyObjs)
    weightTags=[]
    #Gather All the Weight Tags in the scene
    for poly in polyObjs:
        weightTag=poly.GetTag(1019365)
        if weightTag:
            weightTags.append((poly, weightTag))

    #Choose Where to save them all to
    if len(weightTags)==0:
        print("There are no weights to export")

    else:
        fn=c4d.storage.LoadDialog(c4d.FILESELECTTYPE_ANYTHING, "Select A Folder where your weights will be saved", c4d.FILESELECT_DIRECTORY)

        for obj, weightTag in weightTags:
            fn2=os.path.join(fn,obj.GetName())

            with open(fn2,'w') as f:

                f.write(writeHeader())
                f.write(writeJoints(doc, weightTag))
                f.write(writeWeights(obj, weightTag))


if __name__=='__main__':
    main()
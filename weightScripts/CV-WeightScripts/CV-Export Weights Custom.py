"""
Name-US: CV-Export Weights Custom...
Description-US: Export the weights of an object with a custom file name 
"""

import c4d
from os import path
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
        c4d.StatusSetBar(p/op.GetPointCount())
        c4d.StatusSetText(p/op.GetPointCount())

        out = out + "\n" + str(p) + ":"
        # Loop through joints, and write ONLY joints with weight
        for j in range(0, tag.GetJointCount()):
            weight = tag.GetWeight(j, p)

            if weight>0.0:
                out = out + " " + str(j) + " " + str(weight)
    return out

def main():
    Tcaweight = 1019365    # this symbol doesn't seem to be defined

    weightTag = None

    # if that fails, look for the first weight tag on selected object
    if weightTag == None:
        objs = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_0)
        
        if op is not None:
            for tag in op.GetTags():
                #print tag.GetType()
                if tag.GetType() == Tcaweight:
                    weightTag = tag
                    break
    
    # error if we don't have a weight tag
    if weightTag == None:
        return gui.MessageDialog("Please select a weight tag to export")
    else:
        docPath = doc.GetDocumentPath()
        defName = op.GetName()+".w"
        defPath = path.join(docPath,"geo")
        # check if geo subfolder exists
        if path.exists(defPath)==False:
            # what now? create geo or place at doc level?
            defPath = path.join(path.dirname(docPath))
        fn = c4d.storage.SaveDialog(type=c4d.FSTYPE_ANYTHING,
                title="Save Joint Weights for " + op.GetName(),
                def_path=defPath)

        # write the weights
        with open(fn,'w') as f:
            f.write(writeHeader())
            f.write(writeJoints(doc, weightTag))
            c4d.StatusClear()
            f.write(writeWeights(op, weightTag))
            c4d.StatusClear()
            
            


if __name__=='__main__':
    main()

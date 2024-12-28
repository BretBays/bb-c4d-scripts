"""
Name-US: CV-Paste Weights
Description-US: Paste weights onto selected points 
"""

import c4d
from c4d import gui
#Welcome to the world of Python

STORE_WEIGHTS=100291184

def getSelectedPointsList(op):
    listy=[]
    bs=op.GetPointS()
    for index, selected in enumerate(bs.GetAll(op.GetPointCount())):
        if not selected: continue
        else:
            listy.append(index)
    return listy

def pasteJointWeights(obj, weightTag):
    points=getSelectedPointsList(obj)
    bc = c4d.plugins.GetWorldPluginData(STORE_WEIGHTS)
    jointCount=weightTag.GetJointCount()
    
    for point in points:
        
        for jointID in range(jointCount):
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, weightTag)
            weight=bc.GetData(jointID)
            weightTag.SetWeight(jointID, point, weight)
            

def main():
    doc.StartUndo()
    wt=op.GetTag(1019365)
    pasteJointWeights(op, wt)
    wt.WeightDirty()
    doc.EndUndo()
    c4d.EventAdd()
if __name__=='__main__':
    main()

"""
Name-US: CV-Copy Weights
Description-US: Copy the weights of all joint influences on a selected point 
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

def copyJointWeights(obj, weightTag):
    weights=[]
    bc=c4d.BaseContainer()
    points=getSelectedPointsList(obj)
    jointCount=weightTag.GetJointCount()
    
    for jointID in range(jointCount):
        bc.SetData(jointID, weightTag.GetWeight(jointID, points[0]))
        weights.append([jointID, weightTag.GetWeight(jointID, points[0])])
    c4d.plugins.SetWorldPluginData(STORE_WEIGHTS, bc, 0)
        

def main():
    copyJointWeights(op, op.GetTag(1019365))

if __name__=='__main__':
    main()

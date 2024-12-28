"""
Name-US: CV-Hammer Weights
Description-US: Set the selected verts weights to be the average of it's surrounding verts
"""

import c4d
from c4d import gui
#Welcome to the world of Python

def getSelectedPointsList(op):
    listy=[]
    bs=op.GetPointS()
    for index, selected in enumerate(bs.GetAll(op.GetPointCount())):
        if not selected: continue
        else:
            listy.append(index)
    return listy

def MFWH(obj, weightTag, ignoreSelected=True, useEdgeLengths=True):
    pointCount=obj.GetPointCount()
    origSel=c4d.BaseSelect()
    vertList=op.GetPointS()

    vertList.CopyTo(origSel)

    origPoints=getSelectedPointsList(obj)
    jointCount=weightTag.GetJointCount()

    #Original Weights
    weightDict= buildWeightMapDict(weightTag, op)

    for origPoint in origPoints:
        startingSel=c4d.BaseSelect()
        startingSel.DeselectAll()
        startingSel.Select(origPoint)
        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SELECTION, obj)
        startingSel.CopyTo(vertList)

        doc.AddUndo(c4d.UNDOTYPE_CHANGE_SELECTION, obj)
        c4d.utils.SendModelingCommand(c4d.MCOMMAND_SELECTGROW, [obj], c4d.MODELINGCOMMANDMODE_POINTSELECTION)
        listOVerts=getSelectedPointsList(obj)

        if ignoreSelected==True:
            listOVerts.remove(origPoint)

        ratios=calculatePointDistanceRatios(obj, origPoint, listOVerts)
        ratioSum=sum(ratios)

    for map in weightDict.keys():

        #Make a copy of the original map
        newMap=weightDict[map]
        jointID=weightTag.FindJoint(doc.SearchObject(map))
        weightedVals=[]
        for id, vert in enumerate(listOVerts):
            weightedVals.append(weightDict[map][vert]*ratios[id])

        newValue=sum(weightedVals)/ratioSum
        newMap[origPoint]=newValue

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, weightTag)
        weightTag.SetWeightMap(jointID, newMap)





    doc.AddUndo(c4d.UNDOTYPE_CHANGE_SELECTION, obj)
    origSel.CopyTo(vertList)
    c4d.EventAdd()

def buildWeightMapDict(weightTag, obj):
    weightDict={}
    pointCount = obj.GetPointCount()
    for x in range(weightTag.GetJointCount()):
        jointName=weightTag.GetJoint(x).GetName()
        weightDict[jointName]=weightTag.GetWeightMap(x, pointCount)
    return weightDict

def calculatePointDistanceRatios(obj, originIndex, pointIDs):
    originPos=obj.GetPoint(originIndex)

    distances = []
    ratios = []
    for pID in pointIDs:
        pointPos=obj.GetPoint(pID)

        distanceVec = pointPos - originPos
        distances.append(distanceVec.GetLength())


    maxDist = sum(distances)

    for dist in distances:
        ratio = dist / maxDist
        ratios.append(1.0-ratio)

    return ratios

def main():
        #Get the modifier to know what % change we need to do.
    ignoreSelected=True
    useEdgeLengths=True
    doc=c4d.documents.GetActiveDocument()

    bc = c4d.BaseContainer()
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):

        #If CTRL is pressed
        if bc[c4d.BFM_INPUT_QUALIFIER]== 2:
            useEdgeLengths=False
        #If SHIFT is pressed
        if bc[c4d.BFM_INPUT_QUALIFIER]== 1:
            ignoreSelected=False

        #if CTRL+SHIFT is pressed
        elif bc[c4d.BFM_INPUT_QUALIFIER] == 3:
            ignoreSelected=False
            useEdgeLengths=False


    doc.StartUndo()
    wt=op.GetTag(1019365)
    MFWH(op, wt, ignoreSelected, useEdgeLengths)
    wt.WeightDirty()
    doc.EndUndo()

if __name__=='__main__':
    main()
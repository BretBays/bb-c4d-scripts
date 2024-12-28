"""
Name-US: CV-Blend Weights Along Path
Description-US: Create a linear falloff between points along an edge path
"""

import c4d
from c4d import gui
#Welcome to the world of Python

DEBUG=True

def lerp(a, b, t):
    val=a+(b-a)*t
    return val

def getSelectedPointsList(op):
    listy=[]
    bs=op.GetPointS()
    for index, selected in enumerate(bs.GetAll(op.GetPointCount())):
        if not selected: continue
        else:
            listy.append(index)
    return listy

def getEdgeDistance(verts):

    orig=c4d.BaseSelect()

    vertList=op.GetPointS()
    vertList.CopyTo(orig)

    startVert=verts[0]
    endVert=verts[-1]

    s=1
    result=False

    startingSel=c4d.BaseSelect()
    startingSel.DeselectAll()
    startingSel.Select(startVert)

    startingSel.CopyTo(vertList)

    while result is False:
        listOVerts=[]
        #This is where you grow the selection
        c4d.utils.SendModelingCommand(c4d.MCOMMAND_SELECTGROW, [op], c4d.MODELINGCOMMANDMODE_POINTSELECTION)


        for index, selected in enumerate(vertList.GetAll(op.GetPointCount())):
            if not selected: continue

            else:
                listOVerts.append(index)

        if endVert in listOVerts:
            result=True
            break
        else:
            s=s+1
            if s>=20:
                result=True
            else:
                result=False

    orig.CopyTo(vertList)
    return s

def sortVertsByDistance(startVert, verts):
    if startVert in verts:
        verts.remove(startVert)
    orderedPoints=[]
    orderedPoints.insert(0, startVert)

    for vert in verts:
        distance=getEdgeDistance([startVert, vert])
        orderedPoints.insert(distance, vert)

    return orderedPoints

def getLoop(vertList):

    startEndPoints=getStartEndPoints(vertList)
    distance=getEdgeDistance(startEndPoints)
    vertLoop=findByDistance(startEndPoints[0], startEndPoints[1], distance)

    return vertLoop

def getStartEndPoints(verts):
    greatestDistance=0
    for vertA in verts:
        for vertB in verts:
            distance=getEdgeDistance([vertA, vertB])

            if distance>greatestDistance:
                greatestDistance=distance

                if vertA > vertB:
                    pointOrder=[vertA, vertB]
                else:
                    pointOrder=[vertB, vertA]
    return pointOrder

def sortVertsByDistance(startVert, verts):
    if startVert in verts:
        verts.remove(startVert)
    orderedPoints=[]
    orderedPoints.insert(0, startVert)

    for vert in verts:
        distance=getEdgeDistance([startVert, vert])
        orderedPoints.insert(distance, vert)

    return orderedPoints

def findByDistance(start, end, distance):
    opBs=op.GetPointS()
    origBs=c4d.BaseSelect()
    opBs.CopyTo(origBs)
    listy=[]
    points=[start]
    s=distance
    while s>0:
        for point in points:
            bs=c4d.BaseSelect()
            bs.DeselectAll()
            bs.Select(point)
            bs.CopyTo(opBs)
            #Set selection to be point
            for x in range(s):
                c4d.utils.SendModelingCommand(c4d.MCOMMAND_SELECTGROW, [op], c4d.MODELINGCOMMANDMODE_POINTSELECTION)
            #Grow the selection s number of times

            verty=getSelectedPointsList(op)
            if end in verty:
                listy.append(point)
                break

        bs.DeselectAll()
        bs.Select(point)
        bs.CopyTo(opBs)
        c4d.utils.SendModelingCommand(c4d.MCOMMAND_SELECTGROW, [op], c4d.MODELINGCOMMANDMODE_POINTSELECTION)
        #Reset the selection to be start
        points=getSelectedPointsList(op)
        s=s-1

    listy.append(end)
    origBs.CopyTo(opBs)
    return listy

def calculatePointDistanceRatios(obj, originIndex, pointIDs):
    originPos=obj.GetPoint(originIndex)

    distances = []
    ratios = []
    for pID in pointIDs:
        pointPos=obj.GetPoint(pID)

        distanceVec = pointPos - originPos
        distances.append(distanceVec.GetLength())

    startPos=obj.GetPoint(pointIDs[-1])*obj.GetMg()
    endPos=obj.GetPoint(pointIDs[0])*obj.GetMg()
    maxDist = startPos-endPos
    maxLen=maxDist.GetLength()

    for dist in distances:
        ratio = dist / maxLen
        ratios.append(ratio)

    return ratios

def blendWeightAlongPath(interp='linear'):
    doc.StartUndo()
    wt=op.GetTag(1019365)

    jointCount=wt.GetJointCount()
    #Get Start and End Vert Numbers
    verts=getSelectedPointsList(op)
    startWeights=[]
    endWeights=[]
    loopVerts=findByDistance(verts[0], verts[1], getEdgeDistance(verts))

    ratios = calculatePointDistanceRatios(op, loopVerts[0], loopVerts)
    for jointID in range(jointCount):
        startWeights.append(wt.GetWeight(jointID, verts[0]))
        endWeights.append(wt.GetWeight(jointID, verts[1]))

    finalWeights=[]
    for x in range(len(loopVerts)):
        if x>0:
            if interp=='linear':
                percentage=((100.0/(len(loopVerts)-1))/100.0)*x
            elif interp=='edge':
                percentage=ratios[x]
            for jointID in range(jointCount):
                newWeight=lerp(startWeights[jointID], endWeights[jointID], percentage)
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, wt)
                wt.SetWeight(jointID, loopVerts[x], newWeight)

    doc.EndUndo()
    wt.WeightDirty()

def main():
    bc = c4d.BaseContainer()
    interp='edge'
    if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc):

        #if CTRL+SHIFT is pressed
        if bc[c4d.BFM_INPUT_QUALIFIER] == 3:
            interp='linear'
        blendWeightAlongPath(interp)
        c4d.EventAdd()

if __name__=='__main__':
    main()
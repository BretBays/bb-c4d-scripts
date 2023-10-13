import c4d
from c4d import gui
#This script is designed to convert joint weights to a vertex map on an object.
#To use this scrip, simply select your polygon mesh with a weight tag, and the 
#joint or joints you wish to convert to vertex maps. It will then create a vertex
#map per joint named "<jointName>_vmap"


def CopyJointsToVertexMapSelected():
    #You gotta have joints, and a mesh selected

    objs=doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER | c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    joints=[]
    meshes=[]

    for obj in objs:

        if obj.GetType()==c4d.Opolygon:
            meshes.append(obj)
        elif obj.GetType()==1019362:
            joints.append(obj)

    if len(meshes)>0 and len(joints)>0:
        for mesh in meshes:
            wt=mesh.GetTag(1019365)
            if wt:
                for joint in joints:

                    CopyJointToVertexMap(mesh, wt, joint)


def CopyJointToVertexMap(obj, wMap, joint):
    #Gotta find the joint index in wMap
    jointCount=wMap.GetJointCount()
    jointList=[]

    for x in range(jointCount):
        jointList.append(wMap.GetJoint(x))

    if joint in jointList:
        jIndex=jointList.index(joint)


        #Get obj's point count
        pointCount=obj.GetPointCount()

        vMap=obj.MakeVariableTag(c4d.Tvertexmap, obj.GetPointCount())
        obj.InsertTag(vMap)
        doc.AddUndo(c4d.UNDOTYPE_NEW, vMap)
        vMap.SetName(joint.GetName()+"_vmap")
        vMapData=vMap.GetAllHighlevelData()
        for x in range(pointCount-1):
            #print "The Weight Value for point", x, "is",  wMap.GetWeight(jIndex, x)
            vMapData[x]=wMap.GetWeight(jIndex, x)

        #print len(vMapData)
        vMap.SetAllHighlevelData(vMapData)

def main():
    doc.StartUndo()
    CopyJointsToVertexMapSelected()
    doc.EndUndo()
    c4d.EventAdd()
if __name__=='__main__':
    main()
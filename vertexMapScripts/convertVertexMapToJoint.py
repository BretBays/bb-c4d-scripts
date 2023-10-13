import c4d
from c4d import gui
#This Script will take a selection containing a polygon object, a vertex map, and a joint
#and will take the vertex map selected and convert it to joint weights. It assumes your
#poly mesh has a weight tag with the joint already in there. It will handle all normalization
#as well.


def CopyVertexMapToJointSelected():
    #You gotta have joints, and a mesh selected

    objs=doc.GetSelection()
    joints=[]
    meshes=[]
    vmaps=[]

    for obj in objs:
        #Based on our selections, sort each type into it's own list
        if obj.GetType()==c4d.Opolygon:
            meshes.append(obj)
        elif obj.GetType()==1019362:
            joints.append(obj)
        elif obj.GetType()==c4d.Tvertexmap:
            vmaps.append(obj)

    if len(meshes)>0 and len(joints)>0 and len(vmaps)>0:
        for mesh in meshes:
            #From the mesh, get the weight tag. 
            wt=mesh.GetTag(1019365)
            jointIDs=[]
            if wt:
                for id, joint in enumerate(joints):

                    CopyVertexMapToJoint(mesh, wt, vmaps[id], joint)
                    jointIDs.append(c4d.modules.character.CAWeightMgr.GetJointIndex(doc, wt, joint))

                #Normalize town baby
                #Select all of the joints in the weights manager first
                c4d.modules.character.CAWeightMgr.UnselectAllJointListNodes(doc)
                c4d.modules.character.CAWeightMgr.SelectAllJoints(doc)

                #Get the Weight Tag Index:
                wIndex= c4d.modules.character.CAWeightMgr.GetTagIndex(doc, wt)

                for jid in jointIDs:
                    print(jid)
                    c4d.modules.character.CAWeightMgr.UnselectJoint(doc, wIndex, jid[1])

                c4d.modules.character.CAWeightMgr.NormalizeWeights(doc)
                c4d.modules.character.CAWeightMgr.SetDirty(doc)

                c4d.modules.character.CAWeightMgr.Update(doc)
            else:
                c4d.StatusSetText("Unable to find a weight tag on object: {0}".format(mesh.GetName()))

def CopyVertexMapToJoint(obj, wMap, vmap, joint):

    vMapData=vmap.GetAllHighlevelData()

    jIndex=wMap.FindJoint(joint)
    wMap.SetWeightMap(jIndex, vMapData)

def main():
    CopyVertexMapToJointSelected()
    c4d.EventAdd()
if __name__=='__main__':
    main()
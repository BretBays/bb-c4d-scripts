"""
Split Joint 5

Copyright: Bret Bays (www.bretbays.com)
Written for CINEMA 4D R12.021

Name-US: Split Joint 5
Description-US: Splits a Joint into 5
"""


import c4d
from c4d import gui

def GetGlobalPosition(obj):
    return obj.GetMg().off
    

def SetGlobalPosition(obj, pos):
    m=obj.GetMg()
    m.off=pos
    return obj.SetMg(m)

def GetGlobalRotation(obj):
    return c4d.utils.MatrixToHPB(obj.GetMg())

def SetGlobalRotation(obj, rot):
    m=obj.GetMg()
    pos=m.off
    scale=c4d.Vector(m.v1.GetLength(), m.v2.GetLength(), m.v3.GetLength())

    m=c4d.utils.HPBToMatrix(rot)
    
    m.off=pos
    m.v1=c4d.Vector.GetNormalized(m.v1)*scale.x
    m.v2=c4d.Vector.GetNormalized(m.v2)*scale.y
    m.v3=c4d.Vector.GetNormalized(m.v3)*scale.z
    return obj.SetMg(m)


def lerp(a, b, t):
    val=a+(b-a)*t
    return val
    
def main():
    doc.StartUndo()
    factor=0.0
    numJoints=[0]
    ObjList=doc.GetSelection()
    if len(ObjList)!=2:
        gui.MessageDialog("Please Select the 2 Objects you'd like to split between")

    else:
        ObjList=doc.GetSelection()
        StartJnt=ObjList[0]
        EndJnt=ObjList[1]
       
        Startcolor=ObjList[0][c4d.ID_BASEOBJECT_COLOR]
        Endcolor=ObjList[1][c4d.ID_BASEOBJECT_COLOR]
            
        value=5    
        factor=100.0/value/100
            
        StartVec=StartJnt.GetAbsPos()
        EndVec=EndJnt.GetAbsPos()

        s=1
        while (s<=value):
            
            p=s-1

            pos=lerp(StartJnt.GetMg().off, EndJnt.GetMg().off, factor*s)
            numJoints.append(c4d.BaseObject(1019362))

#            numJoints[s].SetAbsPos(lerp(StartVec, EndVec, factor))
            numJoints[s][c4d.ID_BASEOBJECT_COLOR]=lerp(Startcolor, Endcolor, (factor*s))
            numJoints[s].SetName(StartJnt.GetName()+ "_" +str(0)+str(s))

            if s == 1:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, numJoints[s])
                doc.InsertObject(numJoints[s],StartJnt)
                SetGlobalPosition(numJoints[s], pos)
                SetGlobalRotation(numJoints[s], GetGlobalRotation(StartJnt))
            else:
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, numJoints[s])
                doc.InsertObject(numJoints[s], numJoints[p]) 
                SetGlobalPosition(numJoints[s], pos)
                SetGlobalRotation(numJoints[s], GetGlobalRotation(StartJnt))

                            
            doc.AddUndo(c4d.UNDOTYPE_NEW, numJoints[s])
            s=s+1

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, EndJnt)
               
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, EndJnt)
        EndJnt.InsertUnder(numJoints[value-1])

        SetGlobalPosition(EndJnt, numJoints[value].GetMg().off)

        doc.AddUndo(c4d.UNDOTYPE_DELETE, numJoints[value])
        numJoints[value].Remove()   
     
    doc.EndUndo()
    c4d.EventAdd()

    
    

if __name__=='__main__':
    main()
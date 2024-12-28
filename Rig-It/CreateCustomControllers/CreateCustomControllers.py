import c4d
from c4d import gui
#Welcome to the world of Python

def GetGlobalPosition(obj):
    return obj.GetMg().off

def SetGlobalPosition(obj, pos):
    m=obj.GetMg()
    m.off=pos
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    return obj.SetMg(m)

def GetGlobalRotation(obj):
    return c4d.utils.MatrixToHPB(obj.GetMg())

def FreezeObject(obj):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    obj.SetFrozenPos(obj.GetAbsPos())
    obj.SetRelPos(c4d.Vector(0))
    obj.SetFrozenRot(obj.GetAbsRot())
    obj.SetRelRot(c4d.Vector(0))

def SetGlobalRotation(obj, rot):
    m=obj.GetMg()
    pos=m.off
    scale=c4d.Vector(m.v1.GetLength(), m.v2.GetLength(), m.v3.GetLength())

    m=c4d.utils.HPBToMatrix(rot)

    m.off=pos
    m.v1=c4d.Vector.GetNormalized(m.v1)*scale.x
    m.v2=c4d.Vector.GetNormalized(m.v2)*scale.y
    m.v3=c4d.Vector.GetNormalized(m.v3)*scale.z
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    return obj.SetMg(m)

def SetPosRot(obj, obj2):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    SetGlobalPosition(obj, GetGlobalPosition(obj2))
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    SetGlobalRotation(obj, GetGlobalRotation(obj2))
    return obj

def main():
    doc.StartUndo()
    objList=doc.GetSelection()
    splineList=[0]


    if len(objList)==0:
        gui.MessageDialog("Please Select at least One Object")
        return
    else:
        p=0
        while p<len(objList):
            doc.AddUndo(c4d.UNDOTYPE_CHANGE_SELECTION, objList[p])
            p=p+1
        c4d.utils.SendModelingCommand(c4d.MCOMMAND_SELECTALL, objList, mode=c4d.MODELINGCOMMANDMODE_EDGESELECTION, doc=doc)
        c4d.utils.SendModelingCommand(c4d.MCOMMAND_EDGE_TO_SPLINE, objList, doc=doc)
        s=0


        while s<len(objList):

            objName=objList[s].GetName()
            splineList.insert(s, doc.SearchObject(str(objName)+".Spline"))
            if splineList[s] is None:
                s=s+1

            else:
                doc.AddUndo(c4d.UNDOTYPE_NEW, splineList[s])
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, splineList[s])
                splineList[s].InsertBefore(objList[s])
                SetGlobalPosition(splineList[s], GetGlobalPosition(objList[s]))
                SetGlobalRotation(splineList[s], GetGlobalRotation(objList[s]))
                splineList[s][c4d.ID_BASEOBJECT_USECOLOR]=objList[s][c4d.ID_BASEOBJECT_USECOLOR]
                splineList[s][c4d.ID_BASEOBJECT_COLOR]=objList[s][c4d.ID_BASEOBJECT_COLOR]
                doc.AddUndo(c4d.UNDOTYPE_DELETE, objList[s])
                objList[s].Remove()
                s=s+1


    doc.EndUndo()
    c4d.EventAdd()
if __name__=='__main__':
    main()
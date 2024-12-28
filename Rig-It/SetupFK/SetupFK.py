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

def FreezeObject(obj):
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
    obj.SetFrozenPos(obj.GetAbsPos())
    obj.SetRelPos(c4d.Vector(0))
    obj.SetFrozenRot(obj.GetAbsRot())
    obj.SetRelRot(c4d.Vector(0)) 

def lerp(a, b, t):
    val=a+(b-a)*t
    return val
    
def main():

    doc.StartUndo()
    objList=doc.GetSelection()
    spline=5181
    controls=[]
    tags=[]
    s=0
    if len(objList)==0:
        gui.MessageDialog("Please Select an Object") 
    else:  


        while (s<len(objList)):
            
            controls.append(c4d.BaseObject(spline))
            doc.AddUndo(c4d.UNDOTYPE_NEW, controls[s])
            name=objList[s].GetName().split('_bnd_jnt')[0]
            
            name=name+'_CON+'
            constr=c4d.BaseTag(1019364)
            tags.insert(s, constr)
            doc.AddUndo(c4d.UNDOTYPE_NEW, tags[s])
            if s==0:

                doc.InsertObject(controls[s])
                objList[s].InsertTag(tags[s])
                tags[s][c4d.ID_CA_CONSTRAINT_TAG_PSR]=True
                #c4d.CallButton(tags[s], 9000)
                tags[s][10005]=True
                tags[s][10007]=True
                tags[s][10001]=controls[s]

            else:
                doc.AddUndo(c4d.UNDOTYPE_NEW, controls[s])
                doc.InsertObject(controls[s], controls[s-1])
                objList[s].InsertTag(tags[s])
                tags[s][c4d.ID_CA_CONSTRAINT_TAG_PSR]=True
                #c4d.CallButton(tags[s], 9000)
                tags[s][10005]=False
                tags[s][10007]=True
                tags[s][10001]=controls[s]

            controls[s][c4d.PRIM_CIRCLE_RADIUS]=75

            controls[s].SetName(name)

            SetGlobalPosition(controls[s], GetGlobalPosition(objList[s]))

            SetGlobalRotation(controls[s], GetGlobalRotation(objList[s]))
            FreezeObject(controls[s])
            s=s+1
    

    doc.EndUndo()
    c4d.EventAdd()

    
    

if __name__=='__main__':
    main()
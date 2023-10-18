import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    doc.StartUndo()
    objList=doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    for obj in objList:
        if obj != objList[-1]:
            worldMat=obj.GetMg()
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, obj)
            obj.InsertUnder(objList[-1])
            obj.SetMg(worldMat)


    c4d.EventAdd()
    doc.EndUndo()
if __name__=='__main__':
    main()
"""
Group Each

Copyright: Bret Bays (www.bretbays.com)
Written for CINEMA 4D R13.029

Name-US: Group Each
Description-US: Creates a Parent Null for each selected object located at the objects position
"""
import c4d
from c4d import gui



def main():
    doc.StartUndo()
    sel=doc.GetSelection()
    for x in sel:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x)        
        xPos=x.GetMg()
        xPosL=x.GetMl()
        null=c4d.BaseObject(c4d.Onull)
        name=x.GetName()+str("_algn")
        doc.AddUndo(c4d.UNDOTYPE_NEW, null)
        null.SetName(name)

        doc.InsertObject(null, None, x)
        null.SetMg(xPos)
        doc.SetSelection(null, c4d.SELECTION_ADD)
        doc.SetSelection(x, c4d.SELECTION_SUB)
        x.InsertUnder(null)
        x.SetMg(xPos)
        
    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()

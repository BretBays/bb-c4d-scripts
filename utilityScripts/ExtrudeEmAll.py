"""
Extrude 'Em All

Copyright: Bret Bays (www.bretbays.com)
Written for CINEMA 4D R13.029

Name-US: Extrude 'Em All
Description-US: Takes a selection, throws them all into an ExtrudeNURBS and turns on Hierarchy    
"""
import c4d
from c4d import gui



def main():
    sel=doc.GetSelection()
    EN=c4d.BaseObject(c4d.Oextrude)
    EN[c4d.EXTRUDEOBJECT_HIERARCHIC]=1
    doc.InsertObject(EN)
    doc.AddUndo(c4d.UNDOTYPE_NEW, EN)
    doc.SetSelection(EN, c4d.SELECTION_ADD)

    for x in sel:
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, x) 
        x.InsertUnder(EN)
        doc.SetSelection(x, c4d.SELECTION_SUB)        

    c4d.EventAdd()
if __name__=='__main__':
    main()

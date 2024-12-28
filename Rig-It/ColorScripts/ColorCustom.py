"""
Color Custom

Copyright: Bret Bays (www.bretbays.com)
Written for CINEMA 4D R12.021

Name-US: Color Custom
Description-US: Takes a List of Selected Objects and Turns on Use Color, then Allows the user to specify whatever Color they would like
"""

import c4d
from c4d import documents
from c4d import gui
#Welcome to the world of Python

def main():


    doc.StartUndo()
    objList=doc.GetSelection()
    color=gui.ColorDialog(c4d.POPUP_BELOW)
    s=0
    while (s<len(objList)):
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, objList[s])
        objList[s][c4d.ID_BASEOBJECT_USECOLOR]=2
        objList[s][c4d.ID_BASEOBJECT_COLOR]=c4d.Vector(color)
        s=s+1

    doc.EndUndo()
    c4d.EventAdd()



if __name__=='__main__':
    main()
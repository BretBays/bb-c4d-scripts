"""
Color All

Copyright: Bret Bays (www.bretbays.com)
Written for CINEMA 4D R12.021

Name-US: Color All
Description-US: Select All Objects, Run the Script to Automatically color Left, Right, and Center colors
"""

import c4d
from c4d import documents
from c4d import gui
#Welcome to the world of Python

def main():

    #Get all the selected objects
    objList=doc.GetSelection() 
    s=0
    left=[]
    right=[]
    center=[]
    temp=""

    #Iterate through all objects
    while (s<len(objList)):
        #Get the name for each object
        temp=objList[s].GetName()

        #If the first two letters of the name are L_ add it to the left list
        if temp[0:2] == 'L_':
            left.append(objList[s])
            
        #If the first two letters of the name are R_ add it to the right
        elif temp[0:2] == 'R_':
            right.append(objList[s])

        #If it's not the Left or Right it gets added to Center
        else:
            center.append(objList[s])

        s=s+1

    doc.StartUndo()
    
    #Color the Left
    l=0
    while (l<len(left)):
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, left[l])
        left[l][c4d.ID_BASEOBJECT_USECOLOR]=2
        left[l][c4d.ID_BASEOBJECT_COLOR]=c4d.Vector(.118, .196, .902)
        l=l+1 

    #Color the Right
    r=0
    while (r<len(right)):
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, right[r])
        right[r][c4d.ID_BASEOBJECT_USECOLOR]=2
        right[r][c4d.ID_BASEOBJECT_COLOR]=c4d.Vector(.902, .078, .118)
        r=r+1 

    #Color the Center
    c=0
    while (c<len(center)):
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, center[c])
        center[c][c4d.ID_BASEOBJECT_USECOLOR]=2
        center[c][c4d.ID_BASEOBJECT_COLOR]=c4d.Vector(.824, .902, .118)
        c=c+1 

    doc.EndUndo()
    c4d.EventAdd()



if __name__=='__main__':
    main()

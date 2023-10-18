import c4d
import array

def getSelectedPointsList(op):

    #This function provides us with a way to easily get the point IDs that are selected
    listy=[]
    bs=op.GetPointS()
    for index, selected in enumerate(bs.GetAll(op.GetPointCount())):
        if not selected: continue
        else:
            listy.append(index)
    return listy

def invertVertexMap(tag, useComponents=False, selPoints=[]):

    #Get our vertex map data
    data=tag.GetAllHighlevelData()

    if useComponents:
        for point in selPoints:
            data[point]=1.0-data[point]
    else:
        for point in range(len(data)):
            data[point]=1.0-data[point]

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, tag)
    tag.SetAllHighlevelData(data)



def main():
    doc.StartUndo()
    #Clear out the status area because we will use it.
    c4d.StatusClear()

    #First gather the tags
    tags=op.GetTags()

    vmap=None

    #Check to see if there is a vertex map that is selected
    for tag in tags:
        if tag.GetType()==5682 and tag.GetBit(c4d.BIT_ACTIVE)==True:
            #If true, set vmap to the tag and kill the loop
            vmap=tag
            break

    #if we have a vertexmap, we will invert it
    if vmap:

        #Store the mode to determine if we're inverting all or just a selection'
        mode=doc.GetMode()
        invertComponents=False
        selPoints=[]

        #check if the mode is points, edges, or poly
        if mode in [c4d.Mpoints, c4d.Medges, c4d.Mpolygons]:
            invertComponents=True
        if invertComponents:
            #Process the component selections
            if mode == c4d.Medges:

                #Data to convert the edge selection to verts
                bc=c4d.BaseContainer()
                bc[c4d.MDATA_CONVERTSELECTION_LEFT]=1
                bc[c4d.MDATA_CONVERTSELECTION_RIGHT]=0
                c4d.utils.SendModelingCommand(c4d.MCOMMAND_CONVERTSELECTION, [op], c4d.MODELINGCOMMANDMODE_EDGESELECTION, bc)
                c4d.EventAdd()

            elif mode == c4d.Mpolygons:
                bc=c4d.BaseContainer()
                bc[c4d.MDATA_CONVERTSELECTION_LEFT]=2
                bc[c4d.MDATA_CONVERTSELECTION_RIGHT]=0
                c4d.utils.SendModelingCommand(c4d.MCOMMAND_CONVERTSELECTION, [op], c4d.MODELINGCOMMANDMODE_EDGESELECTION, bc)
                c4d.EventAdd()

            #Now that we have converted to points, let's get the selected points we should have'
            selPoints=getSelectedPointsList(op)

            #IF we don't have any selected points(ie you were in a component mode but nothing selected
            #Let's reset invertComponents'
            if len(selPoints)==0:
                invertComponents = False

            #Invert the vertex map
            invertVertexMap(tag, invertComponents, selPoints)
        else:
            invertVertexMap(tag)

    else:

        #If no vertex map selected, say so in the status area.
        c4d.StatusSetText("No Vertex Maps Selected")

    doc.EndUndo()
    c4d.EventAdd()

if __name__=='__main__':
    main()
import c4d
from c4d import gui
#Copyright 2023-Bret Bays

obj=op
use_cache = True
direct_copy = True
GROUPNAME="Ghosts_grp"
LAYERNAME="Ghosts"
MATERIALNAME="Ghost_Material"
MATTAGNAME="Ghost_Material_Texture"
RENDERNAME="Ghost_Render"
SKETCHMATERIAL="Ghost_Sketch"

#-----------------UTILITY FUNCTIONS-----------

def GetChildren(obj, listy):
    '''
    Gets every child that is a child of obj.
    '''
    if obj is None: return

    if obj.GetName()==RENDERNAME:
        listy.append(obj)

    #End Actions
    if (obj.GetDown()):
        GetChildren(obj.GetDown(), listy)
    if (obj.GetNext()):
        GetChildren(obj.GetNext(), listy)

    return listy

def findSketchAndToon(postvid, listy):
    '''
    Gets every child that is a child of obj.
    '''
    if postvid is None: return

    if postvid.GetType()==1011015:
        listy.append(postvid)

    #End Actions
    if (postvid.GetDown()):
        findSketchAndToon(postvid.GetDown(), listy)
    if (postvid.GetNext()):
        findSketchAndToon(postvid.GetNext(), listy)

    return listy


def CSTO(obj):
    '''
    CSTO Takes a deformed object and makes a new mesh of it.
    '''
    op = obj
    mat=op.GetMg()
    if use_cache and op.GetDeformCache():
      op = op.GetDeformCache()

    if direct_copy:
      points = op.GetAllPoints()
      polygons = op.GetAllPolygons()
      dest = c4d.PolygonObject(len(points), len(polygons))
      doc.AddUndo(c4d.UNDOTYPE_NEW, dest)

      doc.AddUndo(c4d.UNDOTYPE_CHANGE, dest)
      dest.SetAllPoints(points)
      for i, p in enumerate(polygons):
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, dest)
        dest.SetPolygon(i, p)
    else:
      dest = op.GetClone(c4d.COPYFLAGS_0)

    doc.InsertObject(dest)
    dest.SetMg(mat)
    dest.Message(c4d.MSG_UPDATE)

    return dest

#-------------END UTILITY FUNCTIONS-----------
#-------------GHOST LAYER FUNCTIONS-----------

def checkForGhostLayer():
  layerRoot=doc.GetLayerObjectRoot()
  layerList = layerRoot.GetChildren()

  for layer in layerList:
    if layer.GetName()==LAYERNAME:
      return layer

  return False

def createGhostLayer():

  ghostLayer = checkForGhostLayer()
  if not ghostLayer:

    ghostLayer = c4d.documents.LayerObject()
    doc.AddUndo(c4d.UNDOTYPE_NEW, ghostLayer)

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, ghostLayer)
    ghostLayer.SetName(LAYERNAME)
    ghostLayerData=ghostLayer.GetLayerData(doc)
    ghostLayerData['color']=c4d.Vector(255.0/255.0, 128/255.0, 0.0)
    ghostLayer.SetLayerData(doc, ghostLayerData)

    ghostLayer.InsertUnder(doc.GetLayerObjectRoot())

  return ghostLayer

  #--------END GHOST LAYER FUNCTIONS----------
  #---------GHOST GROUP FUNCTIONS-------------

def createGhostGroup(layer):

  ghostGroup = checkForGhostGroup()
  if not ghostGroup:

    ghostGroup = c4d.BaseObject(c4d.Onull)
    doc.AddUndo(c4d.UNDOTYPE_NEW, ghostGroup)

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, ghostGroup)
    ghostGroup.SetName(GROUPNAME)

    ghostGroup.SetLayerObject(layer)
    doc.InsertObject(ghostGroup)

  return ghostGroup

def checkForGhostGroup():
  group=doc.SearchObject(GROUPNAME)

  if group:
    return group
  else:
    return False
  #------END GHOST GROUP FUNCTIONS-------------
  #----------GHOST MATERIAL FUNCTIONS----------

def createGhostMaterial():

  ghostMat = checkForGhostMaterial()
  if not ghostMat:
    ghostMat = c4d.BaseMaterial(c4d.Mmaterial)
    doc.AddUndo(c4d.UNDOTYPE_NEW, ghostMat)

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, ghostMat)
    ghostMat.SetName(MATERIALNAME)

    doc.InsertMaterial(ghostMat)

    ghostShader=c4d.BaseShader(c4d.Xcolor)
    ghostShader[c4d.COLORSHADER_COLOR]=c4d.Vector(0)

    ghostMat[c4d.MATERIAL_USE_ALPHA]=True
    ghostMat[c4d.MATERIAL_ALPHA_SHADER]=ghostShader
    ghostMat.InsertShader(ghostShader)
    ghostMat.Message(c4d.MSG_UPDATE)

  return ghostMat

def checkForGhostMaterial():

  ghostMat = doc.SearchMaterial(MATERIALNAME)

  if ghostMat:
    return ghostMat
  else:
    return False

def checkForGroupMaterial(group):
  tags = group.GetTags()
  for tag in tags:
    if tag.GetName()==MATTAGNAME:
      return tag
  return None

def addMaterialToGroup(group, material, layer):

  if group and material and layer:
    ghostMatTag = checkForGroupMaterial(group)
    if not ghostMatTag:
      ghostMatTag = c4d.BaseTag(c4d.Ttexture)
      ghostMatTag.SetLayerObject(layer)
      ghostMatTag[c4d.TEXTURETAG_MATERIAL]=material
      group.InsertTag(ghostMatTag)
      ghostMatTag.SetName(MATTAGNAME)

      return ghostMatTag
  else:
    c4d.gui.MessageDialog("unable to assign material to group")

#------END GHOST MATERIAL FUNCTIONS----------
#----------GHOST RENDER DATA FUNCTIONS-------

def createGhostRenderData(sketchMat):

    rootRenderData = doc.GetFirstRenderData()
    print("ROOT RD", rootRenderData)
    listy=[]
    ghost = GetChildren(rootRenderData, listy)
    print("GHOST", ghost)
    if len(ghost)==0:

        activeRD = doc.GetActiveRenderData()
        print("ACTIVE RD", activeRD)

        rd=c4d.documents.RenderData()
        rd.SetName(RENDERNAME)
        doc.InsertRenderData(rd)

        rd[c4d.RDATA_XRES]=activeRD[c4d.RDATA_XRES]
        rd[c4d.RDATA_YRES]=activeRD[c4d.RDATA_YRES]

        rd[c4d.RDATA_FILMASPECT]=activeRD[c4d.RDATA_FILMASPECT]
        rd[c4d.RDATA_PIXELASPECT]=activeRD[c4d.RDATA_PIXELASPECT]

        sketch = c4d.BaseList2D(1011015)
        rd.InsertVideoPostLast(sketch)
        doc.AddUndo(c4d.UNDOTYPE_NEW, rd)

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, sketch)
        sketch[c4d.OUTLINEMAT_EDLINES_SHOWLINES]=True
        sketch[c4d.OUTLINEMAT_EDLINES_LINE_DRAW]=1
        sketch[c4d.OUTLINEMAT_EDLINES_LINE_OBJECTS_MODE]=0
        sketch[c4d.OUTLINEMAT_EDLINES_REDRAW_FULL]=True

        sketch[c4d.OUTLINEMAT_LINE_CREASE]=0
        sketch[c4d.OUTLINEMAT_LINE_OUTLINE]=1
        sketch[c4d.OUTLINEMAT_LINE_INTERSECTION]=1


        sketch[c4d.OUTLINEMAT_LINE_DEFAULT_MAT_V]=sketchMat

        doc.SetActiveRenderData(rd)

    else:
        lister=[]
        sketch = findSketchAndToon(ghost[0].GetFirstVideoPost(),lister)

        if len(sketch)>0:
            sketch=sketch[0]
        doc.SetActiveRenderData(ghost[0])

    print("SKETCHY", sketch)
    return sketch

def createSketchMaterial():
  sketchMat = doc.SearchMaterial(SKETCHMATERIAL)
  print("SKETCHMAT", sketchMat)
  if not sketchMat:
    sketchMat = c4d.BaseMaterial(1011014)
    doc.AddUndo(c4d.UNDOTYPE_NEW, sketchMat)

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, sketchMat)

    sketchMat.SetName(SKETCHMATERIAL)
    print("SETTING MAT", sketchMat.GetName())

  doc.InsertMaterial(sketchMat)
  return sketchMat

def createGhost(objList, group, layer, material, sketchRD):


    #sketchInList=sketchRD[c4d.OUTLINEMAT_EDLINES_LINE_OBJECTS]
    #print("SKETCHLIST1", sketchInList)

    #if sketchInList==None:)

    #print("SKETCHLIST", sketchInList, sketchInList.GetObjectCount())
    frame = str(doc.GetTime().GetFrame(doc.GetFps()))

    for obj in objList:

        #Let's see if this frame has a ghost already
        currentFrameObj = doc.SearchObject("F_{0}_{1}_ghost".format(frame, obj.GetName()))
        if currentFrameObj:
          currentFrameObj.Remove()

        dupObj = CSTO(obj)
        doc.AddUndo(c4d.UNDOTYPE_NEW, dupObj)

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, dupObj)
        dupObj.SetName("F_{0}_{1}_ghost".format(frame, obj.GetName()))

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, dupObj)
        dupObj.InsertUnder(group)
        dupObj[c4d.ID_LAYER_LINK] = layer

        #Add display tag to prevent it from showing up in renders
        dispTag = c4d.BaseTag(c4d.Tdisplay)
        doc.AddUndo(c4d.UNDOTYPE_NEW, dispTag)

        dupObj.InsertTag(dispTag)

        doc.AddUndo(c4d.UNDOTYPE_CHANGE, dispTag)
        dispTag[c4d.DISPLAYTAG_AFFECT_DISPLAYMODE] = True
        dispTag[c4d.DISPLAYTAG_SDISPLAYMODE]=0


        #Do some logic here to add more stuff to the InExclude

    sketchInList=c4d.InExcludeData()
    print("CHILDREN COUNT",len(group.GetChildren()))
    for child in group.GetChildren():
        sketchInList.InsertObject(child, 1)


    sketchRD[c4d.OUTLINEMAT_EDLINES_LINE_OBJECTS]=sketchInList
    print("SKETCHLIST3", sketchInList, sketchInList.GetObjectCount())


def main():

    doc.StartUndo()
    #Check for and set up everything necessary
    ghostLayer=createGhostLayer()
    ghostGrp=createGhostGroup(ghostLayer)
    ghostMat = createGhostMaterial()
    ghostTex = addMaterialToGroup(ghostGrp, ghostMat, ghostLayer)
    ghostSketchMat = createSketchMaterial()
    ghostRD =  createGhostRenderData(ghostSketchMat)

    print("HERE WE GO")
    objects=[]
    for obj in doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER | c4d.GETACTIVEOBJECTFLAGS_CHILDREN):
    #For now, and for simplicity, let's only function on polygons
        if obj.GetType()==5100:
            objects.append(obj)
    createGhost(objects, ghostGrp, ghostLayer, ghostMat, ghostRD)


    c4d.EventAdd()
    doc.EndUndo()


if __name__=='__main__':
    main()
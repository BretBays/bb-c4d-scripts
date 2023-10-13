import c4d
from c4d import gui
from os import path
#Welcome to the world of Python

def exportVertexMaps(object):
    header="==========Vertex Map Exporter v1.0 by Bret Bays=========="
    vmaps=[]
    tags=object.GetTags()
    for tag in tags:
        if tag.GetType()==c4d.Tvertexmap:
            vmaps.append(tag)

    if len(vmaps)==0:
        return gui.MessageDialog("There were no vertex maps to export on the selected object")
    else:
        docPath = doc.GetDocumentPath()
        defName = object.GetName()+".vmap"
        defPath = path.join(docPath, "geo")
        
        if path.exists(defPath)==False:
            defPath = path.join(path.dirname(docPath))
        
        fn = c4d.storage.SaveDialog(type=c4d.FSTYPE_ANYTHING, title="Save Vertex Maps for " + object.GetName(), def_path=defPath)
        
        with open(fn, 'w') as f:
            f.write(header)

            f.write("\n\n")
            f.write("----------VERTEX MAP WEIGHTS----------\n")
                
            for id2, vmap in enumerate(vmaps):
                weights = vmap.GetAllHighlevelData()
                line = '\n\nVMAP: ' + vmap.GetName() + ' '+ str(id2) + ': ' + str(weights)
                f.write(line)

def main():
    exportVertexMaps(op)

if __name__=='__main__':
    main()

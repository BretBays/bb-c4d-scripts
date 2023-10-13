import c4d
from c4d import gui
#Welcome to the world of Python


def main():
    if doc==None:
        c4d.gui.MessageDialog("There is no active document")
        return
    
    if op==None  or op.CheckType(c4d.Opolygon)==False:
        c4d.gui.MessageDialog("There is no object selected, or the selected object is not a polygon mesh")
        return
    
    fn = c4d.storage.LoadDialog(c4d.FSTYPE_ANYTHING, "Select a Vertex Map File")
    
    if fn!=None:
        mapList = open(fn, "r")
        
        for line in mapList:
            mapLine = line.split()
            #print mapLine
            if len(mapLine) == 0 or line[0]=="#":
                continue

            if mapLine[0] and mapLine[0] == "VMAP:":
                #Create a Vertex Map
                
                
                vmap=c4d.VariableTag(c4d.Tvertexmap, op.GetPointCount())
                vmap.SetName(mapLine[1])
                op.InsertTag(vmap)
                
                weights=mapLine[3:]
                data=[]
                
                for id, weight in enumerate(weights):
                    
                    if id==0:
                        newWeight=weight.split(',')[0]
                        newWeight=newWeight.split('[')[1]
                        newWeight=float(newWeight)
                        data.append(newWeight)
                    elif id==len(weights)-1:
                        newWeight=weight.split(',')[0]
                        newWeight=newWeight.split(']')[0]
                        newWeight=float(newWeight)
                        data.append(newWeight)
                    else:
                        newWeight=weight.split(',')[0]
                        newWeight=float(newWeight)
                        data.append(newWeight)
                        
                curDatas=vmap.GetAllHighlevelData()
                for id, curData in enumerate(curDatas):
                    curDatas[id]=data[id]
                
                vmap.SetAllHighlevelData(curDatas)
                
    c4d.EventAdd()            
    

if __name__=='__main__':
    main()

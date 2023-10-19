import c4d
import array
from operator import add

def main():
    doc.StartUndo()
    c4d.StatusClear()
    #For two vertex map tags, normalize their weights.
    tags=doc.GetActiveTags()
    if len(tags)==2:
        if tags[0].GetType()==5682 and tags[1].GetType()==5682:
            tag1Data=tags[0].GetAllHighlevelData()
            tag2Data=tags[1].GetAllHighlevelData()

            sumData=list(map(add, tag1Data, tag2Data))

            for id, x in enumerate(sumData):
                if x>1.0:
                    inMax=x
                    val1=tag1Data[id]
                    val2=tag2Data[id]
                    result1= c4d.utils.RangeMap(value=val1, mininput=0.0, maxinput=inMax, minoutput=0.0, maxoutput=1.0, clampval=False)
                    result2= c4d.utils.RangeMap(value=val2, mininput=0.0, maxinput=inMax, minoutput=0.0, maxoutput=1.0, clampval=False)
                    tag1Data[id]=result1
                    tag2Data[id]=result2
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, tags[0])
            tags[0].SetAllHighlevelData(tag1Data)
            doc.AddUndo(c4d.UNDOTYPE_CHANGE, tags[1])
            tags[1].SetAllHighlevelData(tag2Data)
            
            op.Message(c4d.MSG_UPDATE)

        else:
            c4d.StatusSetText("Please only select 2 Vertex Maps on the same object")

    else:
        c4d.StatusSetText("Please only select 2 Vertex Maps on the same object")
    
    c4d.DrawViews(c4d.DRAWFLAGS_FORCEFULLREDRAW)
    doc.EndUndo()
    c4d.EventAdd(c4d.EVENT_FORCEREDRAW | c4d.EVENT_ANIMATE)

if __name__=='__main__':
    main()
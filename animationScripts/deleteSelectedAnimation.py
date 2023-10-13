import c4d
from c4d import gui
#Welcome to the world of Python


def deleteSelectedAnimation():
    doc.StartUndo()
    selObjs=doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER)
    if len(selObjs)<=0:
        c4d.StatusSetText("No Objects Selected!")
        return

    doc.SetTime(c4d.BaseTime(0))
    c4d.DrawViews(c4d.DRAWFLAGS_ONLY_ACTIVE_VIEW|c4d.DRAWFLAGS_NO_THREAD|c4d.DRAWFLAGS_STATICBREAK)


    for obj in selObjs:
        tracks=obj.GetCTracks()
        if len(tracks)>0:
            for track in tracks:
                doc.AddUndo(c4d.UNDOTYPE_DELETE, track)
                track.Remove()

    doc.EndUndo()
    c4d.EventAdd()

def main():
    deleteSelectedAnimation()

if __name__=='__main__':
    main()
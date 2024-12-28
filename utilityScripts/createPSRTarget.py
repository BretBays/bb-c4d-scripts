import c4d

doc: c4d.documents.BaseDocument  # The currently active document.
op: c4d.BaseObject | None  # The primary selected object in `doc`. Can be `None`.

def main() -> None:
    """Called by Cinema 4D when the script is being executed.
    """
    doc.StartUndo()
    null = c4d.BaseObject(c4d.Onull)
    doc.InsertObject(null)
    doc.AddUndo(c4d.UNDOTYPE_NEW, null)
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, null)
    null.SetName(op.GetName()+'_targ')
    null.SetMg(op.GetMg())
    
    constraint=c4d.BaseTag(1019364)
    op.InsertTag(constraint)
    doc.AddUndo(c4d.UNDOTYPE_NEW, constraint)

    doc.AddUndo(c4d.UNDOTYPE_CHANGE, constraint)    
    constraint[c4d.ID_CA_CONSTRAINT_TAG_PSR]=True
    constraint[10006]=True
    constraint[10001]=null
    
    doc.EndUndo()
    c4d.EventAdd()

if __name__ == '__main__':
    main()
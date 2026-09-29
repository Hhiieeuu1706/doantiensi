from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V21_TABLES_PRESERVED_FINAL.docx'
dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V22_TABLES_PLACED_FINAL.docx'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; NS={'w':W}
with ZipFile(src,'r') as zin:
    root=etree.fromstring(zin.read('word/document.xml'))
    body=root.find('{%s}body'%W)
    tables=body.xpath('./w:tbl',namespaces=NS)
    targets={}
    for t in tables:
        header=' | '.join(t.xpath('.//w:tr[1]//w:t/text()',namespaces=NS))
        if header.startswith('Protocol | 20% MAE'): targets['protocol']=t
        if header.startswith('Target coverage | Checkpoint'): targets['uncertainty']=t
    # Detach first, then insert immediately after their named captions.
    for t in targets.values(): t.getparent().remove(t)
    for p in list(body):
        text=''.join(p.xpath('.//w:t/text()',namespaces=NS)).strip()
        if text.startswith('Table V15.1.'):
            p.addnext(targets['protocol'])
        elif text.startswith('Table V15.2.'):
            p.addnext(targets['uncertainty'])
    ndoc=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
    with ZipFile(dst,'w',ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data=ndoc if item.filename=='word/document.xml' else zin.read(item.filename)
            zout.writestr(item,data)
print(dst)

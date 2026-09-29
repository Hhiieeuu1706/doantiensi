from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

ROOT=Path(__file__).resolve().parent; pkg=ROOT/'SUBMISSION_PACKAGE_V10'
src=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V19_FIGURE_AUDITED_FINAL.docx'
dst=pkg/'05_manuscript/BATTERY_RUL_PHD_THESIS_V21_TABLES_PRESERVED_FINAL.docx'
img=pkg/'04_results/figures/v21_grouped_features/v21_grouped_state_history_robust.png'
W='http://schemas.openxmlformats.org/wordprocessingml/2006/main'; NS={'w':W}
with ZipFile(src,'r') as zin:
    xml=etree.fromstring(zin.read('word/document.xml'))
    for t in xml.xpath('.//w:t',namespaces=NS):
        if 'Figure V15.2. State and history feature distributions.' in (t.text or ''):
            t.text='Figure V15.2. Grouped robust-scale state and history feature distributions.'
    ndoc=etree.tostring(xml,xml_declaration=True,encoding='UTF-8',standalone=True)
    with ZipFile(dst,'w',ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data=img.read_bytes() if item.filename=='word/media/image4.png' else (ndoc if item.filename=='word/document.xml' else zin.read(item.filename))
            zout.writestr(item,data)
print(dst)

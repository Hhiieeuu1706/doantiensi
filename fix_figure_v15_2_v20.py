from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree

ROOT = Path(__file__).resolve().parent
pkg = ROOT / 'SUBMISSION_PACKAGE_V10'
src = pkg / '05_manuscript' / 'BATTERY_RUL_PHD_THESIS_V19_FIGURE_AUDITED_FINAL.docx'
dst = pkg / '05_manuscript' / 'BATTERY_RUL_PHD_THESIS_V20_FIGURE_CLEAN_FINAL.docx'

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS = {'w': W, 'r': R, 'a': A}

with ZipFile(src, 'r') as zin:
    doc_xml = etree.fromstring(zin.read('word/document.xml'))
    rel_xml = etree.fromstring(zin.read('word/_rels/document.xml.rels'))
    rel_map = {r.get('Id'): r.get('Target') for r in rel_xml}
    remove = []
    for p in doc_xml.xpath('.//w:body/w:p', namespaces=NS):
        embeds = p.xpath('.//a:blip/@r:embed', namespaces=NS)
        if any(rel_map.get(e, '').endswith('media/image4.png') for e in embeds):
            remove.append(p)
        text = ''.join(p.xpath('.//w:t/text()', namespaces=NS))
        if text.strip().startswith('Figure V15.2.'):
            remove.append(p)
    for p in remove:
        p.getparent().remove(p)
    # The former V15.3 becomes V15.2 after the faulty figure is removed.
    for t in doc_xml.xpath('.//w:t', namespaces=NS):
        if 'Figure V15.3.' in (t.text or ''):
            t.text = t.text.replace('Figure V15.3.', 'Figure V15.2.')
    new_doc = etree.tostring(doc_xml, xml_declaration=True, encoding='UTF-8', standalone=True)
    with ZipFile(dst, 'w', ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = new_doc if item.filename == 'word/document.xml' else zin.read(item.filename)
            zout.writestr(item, data)

print(dst)

import sys, re, collections
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import recibos_hoja_unica as B
import pymupdf as fitz, numpy as np
src = fitz.open(sys.argv[1]); out = fitz.open(sys.argv[2])
docs = B.split_docs(src)
def toks(pages):
    t = []
    for p in pages:
        t += [w for w in p.get_text().split() if True]
    return t
bad = 0
for i, (d, op) in enumerate(zip(docs, out)):
    a = [w for w in " ".join(p.get_text() for p in d).split()]
    b = op.get_text().split()
    # drop "Hoja X de Y" footers
    def clean(ws):
        s = " ".join(ws)
        s = re.sub(r"Hoja \d de \d", "", s)
        return sorted(s.split())
    if clean(a) != clean(b):
        bad += 1; print("DIFF doc", i)
print("integridad: docs verificados", len(docs), "con diferencias", bad)
# firma
ys, ori, dup = [], [], []
names = []
margins_bad = 0
for i, p in enumerate(out):
    m = B.ink(p)
    sub = m[int(735*B.SC):int(765*B.SC)]
    best, res = 0, None
    for r in range(sub.shape[0]):
        d = np.diff(np.concatenate(([0], sub[r].astype(np.int8), [0])))
        st = np.where(d == 1)[0]; en = np.where(d == -1)[0]
        if len(st):
            k = (en-st).argmax()
            if en[k]-st[k] > best: best, res = en[k]-st[k], (735+r/B.SC, st[k]/B.SC, en[k]/B.SC)
    y, x0, x1 = res
    ys.append(y)
    t = p.get_text()
    (dup if 'D U P L I C A D O' in t else ori).append(((x0+x1)/2, x1))
    rows = np.where(m.any(axis=1))[0]; cols = np.where(m.any(axis=0))[0]
    bb = (cols[0]/B.SC, rows[0]/B.SC, (cols[-1]+1)/B.SC, (rows[-1]+1)/B.SC)
    if bb[0] < 15 or bb[2] > B.PW-15 or bb[1] < 15 or bb[3] > B.PH-15: margins_bad += 1; print('margen', i, bb)
    names.append(re.search(r"APELLIDO Y NOMBRE\s+(.+)", t).group(1).strip())
print("y firma min/max", round(min(ys),2), round(max(ys),2))
print("ORI centro min/max", round(min(c for c,_ in ori),2), round(max(c for c,_ in ori),2), len(ori))
print("DUP extremo der min/max", round(min(e for _,e in dup),2), round(max(e for _,e in dup),2), len(dup))
print("fuera de margen", margins_bad)
print("empleados unicos", len(set(names)), "paginas", len(out))

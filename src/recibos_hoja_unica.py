import pymupdf as fitz, numpy as np, sys

DPI = 150; SC = DPI / 72.0
PW, PH = 595.92, 842.88
CX0, CX1 = 26.5, 569.5
CW = CX1 - CX0
TOP = 20.0
FIRMA_LINE_Y = 745.0
SIG_CX = PW / 2
SIG_RIGHT = 557.5
SIDE_MIN = 20.0
MIN_GAP = 12.0
PIECE_GAP = 1.5

_cache = {}
def ink(page):
    k = (id(page.parent), page.number)
    if k not in _cache:
        pm = page.get_pixmap(dpi=DPI, colorspace=fitz.csGRAY)
        a = np.frombuffer(pm.samples, dtype=np.uint8).reshape(pm.height, pm.width)
        _cache[k] = a < 248
    return _cache[k]

def groups(page, gap_pt=26):
    m = ink(page); idx = np.where(m.any(axis=1))[0]
    gs, start, prev = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - prev > gap_pt * SC:
            gs.append((start, prev)); start = i
        prev = i
    gs.append((start, prev))
    return [dict(r0=a, r1=b, y0=a / SC, y1=(b + 1) / SC) for a, b in gs]

def line_info(page, g):
    m = ink(page); best, res = 0, None
    for r in range(g['r0'], g['r1'] + 1):
        d = np.diff(np.concatenate(([0], m[r].astype(np.int8), [0])))
        st = np.where(d == 1)[0]; en = np.where(d == -1)[0]
        if len(st):
            k = (en - st).argmax()
            if en[k] - st[k] > best: best, res = en[k] - st[k], (r / SC, st[k] / SC, en[k] / SC)
    return res

def band_x(page, g):
    cols = np.where(ink(page)[g['r0']:g['r1'] + 1].any(axis=0))[0]
    return cols[0] / SC, (cols[-1] + 1) / SC

def tipo_of(pages, lc):
    t = pages[0].get_text()
    if 'D U P L I C A D O' in t: return 'DUP'
    if 'O R I G I N A L' in t: return 'ORI'
    return 'DUP' if lc > PW * 0.6 else 'ORI'

def build_page(out, pages):
    gs0 = groups(pages[0])
    if len(pages) == 1:
        pieces, (spage, sg) = [(pages[0], gs0[0])], (pages[0], gs0[1])
    else:
        gs1 = groups(pages[1])
        pieces, (spage, sg) = [(pages[0], gs0[0]), (pages[1], gs1[0])], (pages[1], gs1[1])

    ly, lx0, lx1 = line_info(spage, sg)
    bx0, bx1 = band_x(spage, sg)
    s_clip = fitz.Rect(bx0 - 2, sg['y0'] - 2.5, bx1 + 2, sg['y1'] + 2.5)
    tipo = tipo_of(pages, (lx0 + lx1) / 2)
    dx = (SIG_CX - (lx0 + lx1) / 2) if tipo == 'ORI' else (SIG_RIGHT - lx1)
    dx = max(SIDE_MIN - s_clip.x0, min(dx, PW - SIDE_MIN - s_clip.x1))
    s_top = FIRMA_LINE_Y - (ly - s_clip.y0)
    s_rect = fitz.Rect(s_clip.x0 + dx, s_top, s_clip.x1 + dx, s_top + s_clip.height)

    clips = []
    for i, (p, g) in enumerate(pieces):
        y0 = TOP if i == 0 else min(TOP, g['y0'] - 1.0)
        clips.append((p, fitz.Rect(CX0, y0, CX1, g['y1'] + 1.5)))
    h_total = sum(c.height for _, c in clips) + PIECE_GAP * (len(clips) - 1)
    s = min(1.0, ((s_top - MIN_GAP) - TOP) / h_total)
    x_left = (PW - CW * s) / 2

    pg = out.new_page(width=PW, height=PH); y = TOP
    for p, c in clips:
        r = fitz.Rect(x_left, y, x_left + CW * s, y + c.height * s)
        pg.show_pdf_page(r, p.parent, p.number, clip=c)
        y = r.y1 + PIECE_GAP * s
    pg.show_pdf_page(s_rect, spage.parent, spage.number, clip=s_clip)
    pg.insert_text((525.6, 820.0), "Hoja 1 de 1", fontname="helv", fontsize=8.5, color=(0.45, 0.48, 0.53))
    return s, tipo

def split_docs(doc):
    k = ['H1' if 'APELLIDO Y NOMBRE' in p.get_text() else 'H2' for p in doc]
    docs, i = [], 0
    while i < len(doc):
        if i + 1 < len(doc) and k[i] == 'H1' and k[i + 1] == 'H2':
            docs.append([doc[i], doc[i + 1]]); i += 2
        else:
            docs.append([doc[i]]); i += 1
    return docs

if __name__ == '__main__':
    doc = fitz.open(sys.argv[1]); out = fitz.open()
    docs = split_docs(doc)
    res = [build_page(out, d) for d in docs]
    out.save(sys.argv[2], garbage=3, deflate=True)
    sc = [r[0] for r in res]
    print(len(doc), '->', len(out), 'hojas | docs', len(docs), '| escala', round(min(sc), 3), '-', round(max(sc), 3))
    import collections
    print(collections.Counter(r[1] for r in res))
    print('escalas <0.75:', [i for i, r in enumerate(res) if r[0] < 0.75])
    print('argmin', min(range(len(sc)), key=lambda i: sc[i]), 'argmax', max(range(len(sc)), key=lambda i: sc[i]))

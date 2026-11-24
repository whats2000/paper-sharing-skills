#!/usr/bin/env python3
"""Measure and check the layout of a deck: where every element really is, and what is out of place.

usage: python3 layout_check.py deck.pptx [--slide N] [--list]

Positions are reported in the 1920 x 1080 px canvas the helpers in slide_kit.py use, so a model can
query real boundaries instead of guessing them. Reports, per slide:
  OFF      an element that runs past the slide edge (or into the footer band) and gets cut off
  OVERLAP  two text-bearing elements that overlap (neither contains the other)
  ARROW    an arrow whose head does not land on a callout or text box (within 24 px)
--list prints every element with its name, box (x, y, w, h) and first words, for querying.
Exit status 1 when anything is reported.
"""
import argparse
import re
import sys

from lxml import etree
from pptx import Presentation

A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS = {'a': A, 'p': P}
FOOTER_TOP = 1040


def elements(slide, k):
    out = []
    for el in slide.shapes._spTree.iterchildren():
        tag = etree.QName(el).localname
        if tag not in ('sp', 'pic', 'cxnSp', 'grpSp', 'graphicFrame'):
            continue
        xf = el.find('.//a:xfrm', NS)
        if xf is None:
            xf = el.find('.//p:xfrm', NS)
        if xf is None or xf.find('a:off', NS) is None:
            continue
        off, ext = xf.find('a:off', NS), xf.find('a:ext', NS)
        box = (int(off.get('x')) / k, int(off.get('y')) / k, int(ext.get('cx')) / k, int(ext.get('cy')) / k)
        name = el.find('.//p:cNvPr', NS).get('name')
        text = ''.join(t.text or '' for t in el.iter('{%s}t' % A)).strip()
        geom = el.find('.//a:prstGeom', NS)
        prst = geom.get('prst') if geom is not None else ('custom' if el.find('.//a:custGeom', NS) is not None else '')
        faded = el.find('.//a:alpha', NS) is not None
        out.append(dict(el=el, tag=tag, name=name, box=box, text=text, prst=prst, faded=faded, flip=xf))
    return out


def head(e, k):
    """arrowhead point of a block arrow or a curved (freeform) arrow, or None."""
    x, y, w, h = e['box']
    d = {'rightArrow': (x + w, y + h / 2), 'leftArrow': (x, y + h / 2),
         'downArrow': (x + w / 2, y + h), 'upArrow': (x + w / 2, y)}
    if e['prst'] in d:
        return d[e['prst']]
    if e['prst'] == 'custom' and e['el'].find('.//a:tailEnd', NS) is not None:
        pts = e['el'].findall('.//a:custGeom//a:pt', NS)
        path = e['el'].find('.//a:custGeom//a:path', NS)
        if pts and path is not None:
            pw, ph = int(path.get('w') or 1), int(path.get('h') or 1)
            lx, ly = int(pts[-1].get('x')), int(pts[-1].get('y'))
            return (x + lx / pw * w if pw else x, y + ly / ph * h if ph else y)
    return None


def inside(pt, box, tol):
    x, y, w, h = box
    return x - tol <= pt[0] <= x + w + tol and y - tol <= pt[1] <= y + h + tol


def overlap(a, b):
    ix = min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0])
    iy = min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1])
    return ix > 4 and iy > 4


def contains(a, b, tol=4):
    return a[0] - tol <= b[0] and a[1] - tol <= b[1] and a[0] + a[2] + tol >= b[0] + b[2] and a[1] + a[3] + tol >= b[1] + b[3]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('deck')
    ap.add_argument('--slide', type=int)
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    prs = Presentation(a.deck)
    k = prs.slide_width / 1920
    W, H = 1920, prs.slide_height / k
    issues = 0
    for i, slide in enumerate(prs.slides, 1):
        if a.slide and i != a.slide:
            continue
        els = elements(slide, k)
        out = []
        if a.list:
            for e in els:
                b = tuple(int(v) for v in e['box'])
                out.append(f'  {e["name"][:24]:24} {str(b):26} {e["prst"][:12]:12} {e["text"][:30]}')
        body = [e for e in els if e['box'][1] < FOOTER_TOP - 2
                and not (e['box'][2] >= W - 4 and e['box'][3] >= H - 4)]      # skip full-slide backgrounds
        for e in body:
            x, y, w, h = e['box']
            if x < -2 or y < -2 or x + w > W + 2 or (y + h > FOOTER_TOP + 2 and y < FOOTER_TOP - 2 and e['tag'] != 'grpSp'):
                out.append(f'  OFF      {e["name"]} {tuple(int(v) for v in e["box"])} {e["text"][:30]}')
        texts = [e for e in body if e['text'] and not e['faded']]
        for m in range(len(texts)):
            for n in range(m + 1, len(texts)):
                p, q = texts[m], texts[n]
                if overlap(p['box'], q['box']) and not contains(p['box'], q['box']) and not contains(q['box'], p['box']):
                    out.append(f'  OVERLAP  "{p["text"][:20]}" / "{q["text"][:20]}"')
                    if len(out) > 30:
                        break
        targets = [e['box'] for e in body if e['text']] + \
                  [e['box'] for e in body if e['prst'] in ('roundRect', 'rect') and not e['text']] + \
                  [e['box'] for e in body if e['tag'] == 'pic']        # flow arrows between pictures
        for e in body:
            pt = head(e, k)
            if pt and not any(inside(pt, b, 24) for b in targets if b != e['box']):
                out.append(f'  ARROW    {e["name"]} head at ({int(pt[0])}, {int(pt[1])}) lands on no callout')
        rep = [o for o in out if not o.startswith('  ') or o[2:10].strip() in ('OFF', 'OVERLAP', 'ARROW')]
        if out:
            print(f'slide {i}')
            print('\n'.join(out))
        issues += sum(1 for o in rep if o[2:10].strip() in ('OFF', 'OVERLAP', 'ARROW'))
    print(f'{issues} issue(s)' if issues else 'no issues')
    sys.exit(1 if issues else 0)


if __name__ == '__main__':
    main()

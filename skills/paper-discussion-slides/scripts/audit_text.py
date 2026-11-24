#!/usr/bin/env python3
"""Audit the on-slide text of a deck from the audience's side.

usage: python3 audit_text.py deck.pptx [--min-size 24] [--caption-size 22] [--max-chars 18]

Reports, per slide:
  SMALL   text runs below --min-size pt (footer band excluded). Runs between --caption-size and
          --min-size are listed as `caption?`: acceptable only for source / figure credits.
  LONG    paragraphs (at body size or larger) that read as sentences rather than keywords: more than --max-chars
          characters (a CJK character counts 1, a Latin word counts 2), or containing
          sentence punctuation (。；, ——, or two or more ，). Titles allow 1.5x the length.
  HOOK    a question line in the lower half of the slide that is visible on the first step of a slide
          (or on a slide with no build steps): a hook for the next slide shown before the speaker reaches it.
          Reveal it as the last step (build_steps). Build steps are recognised by a shared footer page number.
  ARROW   a typed arrow (→ ⇒ ->) in a line of words (CJK text or two or more English words); write the
          connecting word or draw the arrow as a shape. Arrows in equations (no words around them) pass.

Sizes are points on the 20-inch-wide slide the helpers in slide_kit.py write (1920 px canvas);
on a 13.33-inch slide they are scaled to the same proportion before comparing.
Exit status 1 when anything is reported, so it can gate a build.
"""
import argparse
import re
import sys

from pptx import Presentation
from pptx.util import Emu

FOOTER_TOP_PX = 1040          # TEMPLATE['footer']['top'] in slide_kit.py
TITLE_MIN_PT = 44             # runs this large are treated as slide titles


def weight(t):
    """reading length: each CJK char 1, each Latin word 2, digits/punctuation ignored."""
    cjk = sum(1 for c in t if '⺀' <= c <= '鿿' or '豈' <= c <= '﫿')
    words = len(re.findall(r'[A-Za-z]{2,}', t))
    return cjk + 2 * words


def sentence_like(t):
    return bool(re.search(r'[。；]|——', t)) or t.count('，') >= 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('deck')
    ap.add_argument('--min-size', type=float, default=24)
    ap.add_argument('--caption-size', type=float, default=22)
    ap.add_argument('--max-chars', type=int, default=18)
    a = ap.parse_args()

    prs = Presentation(a.deck)
    px = prs.slide_width / 1920                     # EMU per canvas px
    k = Emu(prs.slide_width).inches / 20            # point scale relative to a 20-inch slide
    issues = 0
    pages = []                                       # footer page number of each slide (build steps share one)
    for slide in prs.slides:
        num = None
        for sh in slide.shapes:
            if sh.has_text_frame and sh.top is not None and sh.top / px >= FOOTER_TOP_PX - 2:
                m = re.match(r'\s*(\d+)\s*/\s*\d+\s*$', sh.text_frame.text)
                if m:
                    num = m.group(1)
        pages.append(num)
    for i, slide in enumerate(prs.slides, 1):
        out = []
        first_step = pages[i - 1] is None or i == 1 or pages[i - 2] != pages[i - 1]
        last_step = pages[i - 1] is None or i == len(pages) or pages[i] != pages[i - 1]
        for sh in slide.shapes:
            if not sh.has_text_frame or sh.top is None:
                continue
            if sh.top / px >= FOOTER_TOP_PX - 2:
                continue
            for p in sh.text_frame.paragraphs:
                t = ''.join(r.text for r in p.runs).strip()
                if not t:
                    continue
                sizes = [r.font.size.pt / k for r in p.runs if r.font.size and r.text.strip()]
                big = max(sizes) if sizes else 0
                for r in p.runs:
                    if r.font.size and r.text.strip():
                        s = r.font.size.pt / k
                        if s < a.min_size and len(r.text.strip()) > 2:
                            tag = 'caption?' if s >= a.caption_size else 'SMALL'
                            out.append(f'  {tag:8} {s:4.0f}pt  {r.text.strip()[:40]}')
                limit = a.max_chars * (1.5 if big >= TITLE_MIN_PT else 1)
                w = weight(t)
                if big >= a.min_size and (w > limit or sentence_like(t)):   # captions/credits exempt
                    out.append(f'  LONG     {w:3d}     {t[:60]}')
                if (first_step and big >= a.min_size and big < TITLE_MIN_PT and sh.top / px > 540
                        and re.search(r'[?？]\s*$', t) and not (last_step and len(slide.shapes) <= 4)):
                    out.append(f'  HOOK             {t[:60]}')
                wordy = re.search(r'[\u4e00-\u9fff]', t) or len(re.findall(r'[A-Za-z]{3,}', t)) >= 2
                if wordy and re.search(r'[→⇒⟶]|->|=>', t):
                    out.append(f'  ARROW            {t[:60]}')
        if out:
            print(f'slide {i}')
            print('\n'.join(out))
            issues += sum(1 for o in out if 'caption?' not in o)
    print(f'{issues} issue(s)' if issues else 'no issues')
    sys.exit(1 if issues else 0)


if __name__ == '__main__':
    main()

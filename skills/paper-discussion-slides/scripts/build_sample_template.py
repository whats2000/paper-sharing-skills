"""Build assets/sample-template.pptx: a reference deck for the Beamer Berlin + dolphin template.

It shows the template chrome (header bands, title, footer halves with vertically centred
text) and the standard building blocks: a callout connected by a curved arrow, a red frame
with its red arrow to a callout, a dimming mask over already-discussed content, and two build steps that share one page
number. Open it to see how a finished slide should look, or copy its geometry.

    python build_sample_template.py [out.pptx]
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slide_kit import (new_deck, blank_slide, chrome, text, rect, callout, callout_size, curve_arrow, frame,
                       block_arrow, dim_area, bullets, block, qr, notes, MUTED, BLUE, GRAYBG)

DECK = 'Short Deck Title'
CREDIT = 'Source Authors / Institution, 2026'   # the work being discussed, not the presenter
TOTAL = 3


def placeholder(s, x, y, w, h, label):
    """grey box standing in for a figure or video."""
    els = rect(s, x, y, w, h, fill='DCDCE4', radius=12)
    els += text(s, x, y, w, h, label, size=28, color=MUTED, align='c', anchor='m')
    return els


def cover(prs):
    s = blank_slide(prs)
    text(s, 136, 210, 1648, 180, 'Talk Title in the Slide Language', size=60, color='3333B2', align='c', anchor='m')
    text(s, 360, 405, 1200, 68, 'Original Paper / Article Title', size=32, color='3333B2', align='c')
    text(s, 360, 490, 1200, 60, 'Authors · Venue or Source Type · Date', size=26, align='c')
    placeholder(s, 460, 600, 1000, 260, 'cover strip: figures from the source')
    text(s, 1000, 940, 840, 90, ['Presented by Presenter Name', 'Presenter Institution'], size=24, align='r')
    notes(s, 'Cover: no header or footer. Title in the talk language; original title, authors, source type and date below; '
             'the presenter goes bottom right. The footer credit on later slides names the source authors.')
    return s


def content(prs, step):
    s = blank_slide(prs)
    chrome(s, 'Topic or question, not the answer', DECK, CREDIT, page=2, total=TOTAL)
    fig = placeholder(s, 72, 240, 1000, 560, 'figure from the source')
    text(s, 72, 820, 1000, 40, 'Fig. N  caption in muted grey; "redrawn from the paper\'s Fig. N data" if redrawn',
         size=20, color=MUTED)
    if step == 1:
        _, b = callout(s, 1180, 250, ['A question that makes', 'the audience think?'])
        curve_arrow(s, (72, 240, 1000, 560), b)
        notes(s, 'Build step 1 of 2 (same page number as step 2). The callout is pulled out on a slant, so the arrow '
                 'curves: straight out of the figure\'s right edge, straight into the callout\'s bottom edge.')
    else:
        dim_area(s, 72, 240, 1000, 560)   # mask over what step 1 discussed
        f = (300, 420, 360, 220)
        rect(s, f[0], f[1], f[2], f[3], fill='C9D7EA', radius=12)
        frame(s, *f)
        cw, ch = callout_size(['This part means …'])
        _, b = callout(s, 1180, f[1] + f[3] / 2 - ch / 2, ['This part means …'])
        curve_arrow(s, f, b)
        notes(s, 'Build step 2 of 2: the previous callout and arrow are gone; the figure is dimmed with dim_area() only '
                 'to show the mask (white, 80% opacity, no outline, no shadow); normally a frame circles part of an '
                 'image and nothing is dimmed. The callout is lined up with the frame, so the arrow is straight.')
    return s


def blocks(prs):
    s = blank_slide(prs)
    chrome(s, 'Block element (layout is chosen per slide)', DECK, CREDIT, page=3, total=TOTAL)
    for i, (head, body) in enumerate([('Block A', ['keyword or number', 'second keyword']),
                                      ('Block B', ['keyword or number', 'second keyword'])]):
        block(s, 72 + i * 900, 260, 840, 450, head, body, size=30)
    qr(s, '', 1620, 740, 200, label='Slido QR (placeholder)')
    notes(s, 'block() in the template colours; headings and columns are placeholders. '
             'The QR placeholder shows what qr() draws when no event link is known yet.')
    return s


def main(out):
    prs = new_deck()
    cover(prs)
    content(prs, 1)
    content(prs, 2)
    blocks(prs)
    prs.save(out)
    print('wrote', out)


if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, '..', 'assets', 'sample-template.pptx'))

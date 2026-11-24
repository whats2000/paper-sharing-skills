"""slide_kit: python-pptx helpers for paper-discussion slides.

All coordinates are in a 1920 x 1080 pixel canvas and are scaled to the real slide width,
so the same numbers work for any 16:9 template. Font sizes are given in points on that canvas
(1 px = 0.75 pt, i.e. a 20-inch-wide slide) and are scaled the same way, so a 36 pt callout keeps
the same proportion on a 13.33-inch slide. Every drawing function returns the XML
elements it created (so they can be passed to `dim`), and callout / picture also return
the box they occupy (so arrows and frames can be placed from it).

Requires: python-pptx, Pillow
"""
from pptx.util import Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from PIL import Image

# colours (override to match your template)
INK = '1A1A1A'
MUTED = '5F5F6E'
BLUE = '3333B2'
RED = 'C83C3C'
GRAYBG = 'F0F0F0'
CALLRED = 'FF5757'
CALLLINE = '99BDD9'
ARROWGRAY = 'C8D0DA'
LATIN_FONT = 'Arial'
EA_FONT = 'Microsoft JhengHei'
RADIUS = 14

_CANVAS_W = 1920


def _scale(slide):
    return slide.part.package.presentation_part.presentation.slide_width / _CANVAS_W


def _px(slide, v):
    return Emu(int(v * _scale(slide)))


def _font_scale(slide):
    return _scale(slide) / 9525   # 9525 EMU per px on a 20-inch-wide slide


def _style_run(r, size, color, bold, italic=False, mono=False, k=1.0):
    f = r.font
    f.size = Pt(size * k)
    f.bold = bold
    f.italic = italic
    f.color.rgb = RGBColor.from_string(color)
    f.name = 'Courier New' if mono else LATIN_FONT
    rPr = r._r.get_or_add_rPr()
    ea = rPr.find(qn('a:ea'))
    if ea is None:
        ea = rPr.makeelement(qn('a:ea'), {})
        rPr.append(ea)
    ea.set('typeface', EA_FONT)


def text(slide, x, y, w, h, paras, size=24, color=INK, bold=False, align='l', anchor='t', mono=False, italic=False):
    """paras: str | [str, ...] | [[(text, {size, color, bold, italic}), ...], ...]"""
    tb = slide.shapes.add_textbox(_px(slide, x), _px(slide, y), _px(slide, w), _px(slide, h))
    tf = tb.text_frame
    tf.word_wrap = True
    for m in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'):
        setattr(tf, m, 0)
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    if isinstance(paras, str):
        paras = [paras]
    for i, para in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[align]
        segs = [(para, {})] if isinstance(para, str) else para
        for t, o in segs:
            r = p.add_run()
            r.text = t
            _style_run(r, o.get('size', size), o.get('color', color), o.get('bold', bold), o.get('italic', italic), mono, _font_scale(slide))
    return [tb._element]


def rect(slide, x, y, w, h, fill=GRAYBG, line=None, line_w=1.5, radius=RADIUS, shape=None):
    if shape is None:
        shape = MSO_SHAPE.ROUNDED_RECTANGLE if (radius and min(w, h) >= 24) else MSO_SHAPE.RECTANGLE
    sp = slide.shapes.add_shape(shape, _px(slide, x), _px(slide, y), _px(slide, w), _px(slide, h))
    if shape in (MSO_SHAPE.ROUNDED_RECTANGLE, MSO_SHAPE.ROUND_2_SAME_RECTANGLE):
        sp.adjustments[0] = min(0.5, radius / min(w, h))
    sp.shadow.inherit = False
    if fill:
        sp.fill.solid()
        sp.fill.fore_color.rgb = RGBColor.from_string(fill)
    else:
        sp.fill.background()
    if line:
        sp.line.color.rgb = RGBColor.from_string(line)
        sp.line.width = Pt(line_w * _font_scale(slide))
    else:
        sp.line.fill.background()
    return [sp._element]


def text_width(t, size):
    """approximate rendered width in px of one line at `size` pt (CJK = 1 em, Latin ≈ 0.56 em)."""
    em = size / 0.75
    return sum(em * (0.56 if ord(c) < 0x2E80 else 1.0) for c in t)


def callout_size(lines, size=36, w=None):
    """(w, h) the callout box will have, so it can be positioned before it is drawn."""
    lh = size / 0.75 * 1.3
    padx, pady = 40, 26
    if w is None:
        w = max(text_width(l, size) for l in lines) + 2 * padx
    return w, lh * len(lines) + 2 * pady


def callout(slide, x, y, lines, size=36, w=None, align='c', anchor=None, valign='t'):
    """red bold callout whose box fits its text.
    anchor: None / 'l' -> x is the left edge, 'r' -> x is the right edge, 'c' -> x is the centre.
    valign: 't' -> y is the top edge, 'm' -> y is the vertical centre, 'b' -> y is the bottom edge.
    returns (elements, (x, y, w, h))."""
    padx = 40
    w, h = callout_size(lines, size, w)
    if anchor == 'r':
        x -= w
    elif anchor == 'c':
        x -= w / 2
    if valign == 'm':
        y -= h / 2
    elif valign == 'b':
        y -= h
    els = rect(slide, x, y, w, h, fill=GRAYBG, line=CALLLINE, line_w=1.5, radius=16)
    els += text(slide, x + padx * 0.5, y, w - padx, h, lines, size=size, color=CALLRED, bold=True, align=align, anchor='m')
    return els, (x, y, w, h)


def frame(slide, x, y, w, h, color=CALLRED, width=6):
    """red frame around part of an image."""
    return rect(slide, x, y, w, h, fill=None, line=color, line_w=width, radius=16)


def sub(box, tl, br, pad=6):
    """box = (x, y, w, h) covered by an image; tl / br = fractions measured on the ORIGINAL asset."""
    x, y, w, h = box
    return (x + tl[0] * w - pad, y + tl[1] * h - pad, (br[0] - tl[0]) * w + 2 * pad, (br[1] - tl[1]) * h + 2 * pad)


def picture(slide, path, x, y, w, h, alt=''):
    """place an image inside (x, y, w, h) keeping its aspect ratio ('contain').
    returns (elements, box actually covered by the image)."""
    with Image.open(path) as im:
        r = im.width / im.height
    if w / h > r:
        nw = h * r
        X, Y, W, H = x + (w - nw) / 2, y, nw, h
    else:
        nh = w / r
        X, Y, W, H = x, y + (h - nh) / 2, w, nh
    pic = slide.shapes.add_picture(path, _px(slide, X), _px(slide, Y), _px(slide, W), _px(slide, H))
    pic._element.find('.//' + qn('p:cNvPr')).set('descr', alt)
    return [pic._element], (X, Y, W, H)


def arc_arrow(slide, p0, p1, bend=0.35, color=CALLRED, width=10, n=32):
    """curved red arrow from p0 to p1 (px), arrowhead at p1. bend > 0 bows to the left of the travel direction; ~0 is straight.
    For a callout, p0 is on the element being discussed and p1 on the callout: red means the point is pulled out for discussion."""
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * bend, my + dx * bend
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
                    (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1))
    fb = slide.shapes.build_freeform(_px(slide, pts[0][0]), _px(slide, pts[0][1]), scale=1.0)
    fb.add_line_segments([(_px(slide, a), _px(slide, b)) for a, b in pts[1:]], close=False)
    sp = fb.convert_to_shape()
    sp.fill.background()
    sp.shadow.inherit = False
    sp.line.color.rgb = RGBColor.from_string(color)
    sp.line.width = Pt(width * _font_scale(slide))
    ln = sp._element.find('.//' + qn('a:ln'))
    ln.set('cap', 'rnd')
    ln.append(ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'}))
    return [sp._element]


def block_arrow(slide, x, y, w, h, direction='down', fill=ARROWGRAY):
    """solid block arrow for a direct 'this, therefore' link. For a callout it points from the element to the callout
    (direction names where the head points); also used for flow between parts of the content."""
    shp = {'down': MSO_SHAPE.DOWN_ARROW, 'right': MSO_SHAPE.RIGHT_ARROW,
           'left': MSO_SHAPE.LEFT_ARROW, 'up': MSO_SHAPE.UP_ARROW}[direction]
    sp = slide.shapes.add_shape(shp, _px(slide, x), _px(slide, y), _px(slide, w), _px(slide, h))
    sp.fill.solid()
    sp.fill.fore_color.rgb = RGBColor.from_string(fill)
    sp.line.fill.background()
    sp.shadow.inherit = False
    return [sp._element]


def dim(elements, amt=30000):
    """make elements semi-transparent (pictures, fills, lines, text). amt: 0–100000 opacity."""
    for el in elements:
        if el is None:
            continue
        for b in el.iter(qn('a:blip')):
            if b.find(qn('a:alphaModFix')) is None:
                b.insert(0, b.makeelement(qn('a:alphaModFix'), {'amt': str(amt)}))
        for c in el.iter(qn('a:srgbClr')):
            if c.find(qn('a:alpha')) is None:
                c.append(c.makeelement(qn('a:alpha'), {'val': str(amt)}))
    return elements


def _plain(el):
    """drop the shape's theme style reference, so no renderer adds a theme shadow or outline
    (a shadow under a semi-transparent white mask shows through as a grey box)."""
    st = el.find(qn('p:style'))
    if st is not None:
        el.remove(st)


def dim_area(slide, x, y, w, h, fill='FFFFFF', opacity=80000):
    """fade a region that was ALREADY discussed: a white mask over it (default for dimming).

    One rectangle, `opacity` 80000 (= PowerPoint transparency 20%), no outline, no shadow, so the
    earlier content stays readable for context while the eye goes to the current part. Cover a
    whole group (picture + text + arrow of one row) with one mask. Because each build step is its
    own slide, the effect survives PDF export. Opposite of `hide`, which covers what is still to come;
    use `dim` only to fade a single element in place. Draw it after the content it covers."""
    els = rect(slide, x, y, w, h, fill=fill, radius=0)
    for c in els[0].iter(qn('a:srgbClr')):
        c.append(c.makeelement(qn('a:alpha'), {'val': str(opacity)}))
    _plain(els[0])
    return els


def hide(slide, x, y, w, h, fill='FFFFFF', opacity=100000):
    """cover a part of an image that has NOT been explained yet (build by subtraction on a single image).

    This is the opposite of `dim`: `dim` fades what was already discussed, `hide` covers what is
    still to come. Prefer cropping or splitting the image into its parts when the parts are
    separable; use `hide` when they are not. Remove the cover on the step that explains that part."""
    els = rect(slide, x, y, w, h, fill=fill, radius=0)
    for c in els[0].iter(qn('a:srgbClr')):
        c.append(c.makeelement(qn('a:alpha'), {'val': str(opacity)}))
    _plain(els[0])
    return els


def hbars(slide, x, y, rows, label_w=560, bar_w=760, vmax=100, vmin=0, bar_h=60, gap=34, size=26, track=False,
          axis_color='5F5F6E'):
    """native horizontal bar chart. rows: [(label, value, colour, value_text), ...].

    Negative values are supported: set vmin < 0 (e.g. vmin=-2000, vmax=16000). The zero line is
    drawn and bars grow left or right from it. Positive values are labelled just outside the bar end;
    negative values just right of the zero line, so labels never collide with the row labels.
    returns {label: (bar_x, bar_y, bar_w, bar_h, value_text_outer_edge)} with bar_x the left edge."""
    out = {}
    span = vmax - vmin
    bx0 = x + label_w
    zx = bx0 + bar_w * (0 - vmin) / span
    n = len(rows)
    if vmin < 0:
        rect(slide, zx - 1.5, y - 10, 3, n * (bar_h + gap) - gap + 20, fill=axis_color, radius=0)
    for i, (lab, v, col, vt) in enumerate(rows):
        yy = y + i * (bar_h + gap)
        text(slide, x, yy, label_w - 24, bar_h, lab, size=size, align='r', anchor='m')
        if track:
            rect(slide, bx0, yy, bar_w, bar_h, fill='E6E6EC', radius=0)
        bw = max(4, bar_w * abs(v) / span)
        left = zx if v >= 0 else zx - bw
        rect(slide, left, yy, bw, bar_h, fill=col, radius=0)
        tw = text_width(vt, size + 2)
        if v >= 0:
            vx = (bx0 + bar_w if track else left + bw) + 18
            text(slide, vx, yy, tw + 20, bar_h, vt, size=size + 2, bold=True, anchor='m')
            edge = vx + tw
        else:                              # right of the zero line, so it never collides with the row label
            vx = zx + 18
            text(slide, vx, yy, tw + 20, bar_h, vt, size=size + 2, bold=True, anchor='m')
            edge = vx + tw
        out[lab] = (left, yy, bw, bar_h, edge)
    return out


def box_of(el, slide=None):
    """(x, y, w, h) in px of one shape element (sp, pic, cxnSp, graphicFrame or group), or None."""
    xf = el.find('.//' + qn('a:xfrm'))
    if xf is None:
        xf = el.find('.//' + qn('p:xfrm'))
    if xf is None:
        return None
    off, ext = xf.find(qn('a:off')), xf.find(qn('a:ext'))
    if off is None or ext is None:
        return None
    k = 9525.0 if slide is None else _scale(slide)
    return (int(off.get('x')) / k, int(off.get('y')) / k, int(ext.get('cx')) / k, int(ext.get('cy')) / k)


def bbox(elements, slide=None, pad=0):
    """union (x, y, w, h) in px of several shape elements, grown by `pad` on every side."""
    bs = [b for b in (box_of(e, slide) for e in elements if e is not None) if b]
    if not bs:
        return None
    x0 = min(b[0] for b in bs) - pad
    y0 = min(b[1] for b in bs) - pad
    x1 = max(b[0] + b[2] for b in bs) + pad
    y1 = max(b[1] + b[3] for b in bs) + pad
    return (x0, y0, x1 - x0, y1 - y0)


CONTENT = dict(x0=48, y0=215, x1=1872, y1=1025)   # area below the title and above the footer


def annotate(slide, target, lines, side='below', kind='therefore', gap=80, size=36, frame_target=False, outside=None):
    """explain one thing with a callout: target -> arrow -> callout, drawn as ONE unit.

    target: (x, y, w, h) px of what is being explained (a bar, a point, part of a figure);
    side:   where the callout goes: 'below', 'above', 'right' or 'left' of the target;
    kind:   'therefore' = solid grey-blue block arrow (a direct consequence),
            'discuss'   = red curved arrow (the point is pulled out for discussion).
    The callout is centred on the target along that side and kept inside the content area, and the
    arrow runs from the target's edge to the middle of the callout's facing edge, so the arrowhead
    always lands on the callout (reading order: figure first, then the explanation).
    frame_target=True also draws a red frame around the target.
    outside: (x, y, w, h) of the figure the target sits in (e.g. the chart's box from picture()).
    The callout is then placed just outside that figure on `side`, still lined up with the target,
    so it never hides the data; the arrow runs straight over the figure along the shortest path.
    Without it the callout sits `gap` px from the target, which can cover the figure.
    Returns (elements, callout_box); pass the elements to build_steps() as one part with box
    'remove', so the frame, the arrow and the callout appear together and leave together when
    the focus moves on."""
    tx, ty, tw, th = target
    cw, ch = callout_size(lines, size)
    C = CONTENT
    if kind == 'discuss':
        gap = max(gap, 120)                      # a curve needs room, or it shrinks to a squiggle
    ox, oy, ow, oh = outside if outside else target
    g = 40 if outside else gap
    if side in ('below', 'above'):
        cx = tx + tw / 2 - cw / 2
        cy = oy + oh + g if side == 'below' else oy - g - ch
    else:
        cy = ty + th / 2 - ch / 2
        cx = ox + ow + g if side == 'right' else ox - g - cw
    cx = max(C['x0'], min(cx, C['x1'] - cw))
    cy = max(C['y0'], min(cy, C['y1'] - ch))
    els = []
    if frame_target:
        els += frame(slide, *target)
    cel, cbox = callout(slide, cx, cy, lines, size=size)
    cx, cy, cw, ch = cbox
    m = 8
    if side in ('below', 'above'):
        lo, hi = max(tx, cx), min(tx + tw, cx + cw)
        ax = (lo + hi) / 2 if hi > lo else cx + cw / 2
        y0, y1 = (ty + th + m, cy - m) if side == 'below' else (ty - m, cy + ch + m)
        if kind == 'therefore':
            top, h = min(y0, y1), abs(y1 - y0)
            els += block_arrow(slide, ax - 30, top, 60, h, 'down' if side == 'below' else 'up')
        else:
            els += arc_arrow(slide, (tx + tw / 2, y0), (cx + cw / 2, y1), bend=0.25)
    else:
        lo, hi = max(ty, cy), min(ty + th, cy + ch)
        ay = (lo + hi) / 2 if hi > lo else cy + ch / 2
        x0, x1 = (tx + tw + m, cx - m) if side == 'right' else (tx - m, cx + cw + m)
        if kind == 'therefore':
            left, w = min(x0, x1), abs(x1 - x0)
            els += block_arrow(slide, left, ay - 30, w, 60, 'right' if side == 'right' else 'left')
        else:
            els += arc_arrow(slide, (x0, ty + th / 2), (x1, cy + ch / 2), bend=0.25)
    els += cel       # callout last, so it sits on top of the arrow's tip
    return els, cbox


def _outline_only(el):
    """True for a shape drawn only by its outline (a red frame, a curved arrow): fade it, do not mask it."""
    sp = el.find(qn('p:spPr'))
    if sp is None or el.tag != qn('p:sp'):
        return False
    return sp.find(qn('a:solidFill')) is None and el.find('.//' + qn('a:t')) is None


def build_steps(prs, draw, steps, scripts=None):
    """Make the build steps of one slide the way a designer does by hand: build the complete slide,
    copy it once per step, delete from each copy what has not been said yet, and lay a mask over
    what was already discussed so the eye goes to the current part.

    draw(slide) draws the COMPLETE slide (call chrome() inside it, with the same page for every
    step) and returns a list of parts, each a tuple (elements, box, appear, focus_end):
      elements   the XML elements a drawing function returned (callout, picture, text, arrow, ...);
      box        what happens once the part is no longer the focus:
                 'remove' for annotations: a callout with its arrow and frame (what annotate()
                 returns) leaves with its step; it does not stay on later steps, faded or not;
                 'auto' for content already discussed (a picture, a list item, a block): each
                 filled element gets its own tight mask so it stays readable but quiet, and
                 outline-only elements fade in place; or an explicit (x, y, w, h) in px; or None to never
                 mask the part. Put a frame, its arrow and its callout in ONE part (annotate()
                 returns them together) so they fade together;
      appear     the first step (1-based) on which the part is shown;
      focus_end  the last step on which the part is the focus; on later steps a dim_area() mask
                 covers its box. None = never dimmed.
    Anything draw() creates that is not in a part is shown on every step.
    scripts: optional list of speaker scripts, one per step.
    Masks never cover what is current: after the masks are drawn, the parts that are still the
    focus are moved back on top. A warning is printed when a mask would cut through an element
    that is not being faded, so check those steps.
    Returns the list of step slides. Because every step is its own slide, the build survives
    export to PDF and handouts."""
    out = []
    for k in range(1, steps + 1):
        s = blank_slide(prs)
        parts = draw(s) or []
        masks, faded, live = [], set(), []
        for els, box, appear, focus_end in parts:
            gone = box == 'remove' and focus_end is not None and focus_end < k
            if appear > k or gone:
                for e in els:
                    if e is not None and e.getparent() is not None:
                        e.getparent().remove(e)
            elif focus_end is not None and focus_end < k and box:
                if box == 'auto':                # one tight mask per filled element; outlines fade in place
                    for e in els:
                        if e is None:
                            continue
                        if _outline_only(e):
                            dim([e], 25000)
                        else:
                            b = box_of(e, s)
                            if b:
                                masks.append((b[0] - 4, b[1] - 4, b[2] + 8, b[3] + 8))
                else:
                    masks.append(box)
                faded.update(id(e) for e in els if e is not None)
            else:
                live.append(els)
        vids = _VIDEOS.get(id(s._element))
        if vids:                                   # drop removed videos from the slide timing
            alive = {e.get('id') for e in s._element.iter(qn('p:cNvPr'))}
            _VIDEOS[id(s._element)] = [v for v in vids if v[0] in alive]
            _video_timing(s)
        tree = s.shapes._spTree
        for b in masks:
            dim_area(s, *b)
            for e in list(tree):
                if id(e) in faded or e.tag not in (qn('p:sp'), qn('p:pic'), qn('p:cxnSp'), qn('p:grpSp')):
                    continue
                eb = box_of(e, s)
                if not eb or eb[1] * 1 >= 1035 or eb[3] <= 0:
                    continue
                ix = min(b[0] + b[2], eb[0] + eb[2]) - max(b[0], eb[0])
                iy = min(b[1] + b[3], eb[1] + eb[3]) - max(b[1], eb[1])
                inside = ix >= eb[2] - 2 and iy >= eb[3] - 2
                live_ids = {id(x) for els in live for x in els if x is not None}
                has_text = e.find('.//' + qn('a:t')) is not None
                if (ix > 2 and iy > 2 and not inside and e.find('.//' + qn('a:alpha')) is None
                        and (id(e) in live_ids or has_text)):
                    name = e.find('.//' + qn('p:cNvPr')).get('name')
                    print(f'build_steps: step {k}: mask {tuple(int(v) for v in b)} cuts through "{name}"')
        for els in live:                         # current parts back on top of every mask
            for e in els:
                if e is not None and e.getparent() is tree:
                    tree.remove(e)
                    ext = tree.find(qn('p:extLst'))
                    if ext is not None:
                        ext.addprevious(e)
                    else:
                        tree.append(e)
        if scripts:
            notes(s, scripts[k - 1])
        out.append(s)
    return out


def notes(slide, script):
    """speaker notes (write the full spoken script here)."""
    slide.notes_slide.notes_text_frame.text = script


# ---------------------------------------------------------------------------
# Template chrome: header, title and footer (Beamer Berlin + dolphin, measured)
# ---------------------------------------------------------------------------
# Every value is in the 1920 x 1080 canvas. Change TEMPLATE to match another
# template after measuring it (see references/template-example.md).
TEMPLATE = {
    'header': [(0, 46, '4747BA'), (46, 88, '8585D1')],   # (top, bottom, colour) bands
    'title': dict(x=72, y=120, w=1776, h=78, size=48, color='3333B2'),
    'footer': dict(top=1040, bottom=1080, split=960,
                   left_fill='4747BA', right_fill='8585D1',
                   left_color='FFFFFF', right_color='1F1F5C', size=18, pad=36),
    'block': dict(title_fill='4747BA', title_color='FFFFFF', body_fill='EBEBF7', title_h=70, size=32),
}


def new_deck(template_path=None):
    """open a template PPTX, or create an empty 16:9 deck (20 x 11.25 in, i.e. 1 px = 9525 EMU)."""
    from pptx import Presentation
    prs = Presentation(template_path) if template_path else Presentation()
    if not template_path:
        prs.slide_width, prs.slide_height = Emu(18288000), Emu(10287000)
    return prs


def blank_slide(prs):
    """add a slide on the layout with the fewest placeholders and remove any placeholders it brings."""
    layout = min(prs.slide_layouts, key=lambda l: len(l.placeholders))
    s = prs.slides.add_slide(layout)
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    return s


def band_text(slide, x, y, w, h, t, size, color, align='l', bold=False):
    """one line of text centred vertically inside a band.

    The text box is exactly the band (same top and height), has zero insets, does not
    autofit, and is anchored in the middle, so the baseline cannot drift above the band.
    Footer text that sits too high is almost always a text box that is taller than the
    band, starts above it, or is anchored to the top with default insets."""
    els = text(slide, x, y, w, h, t, size=size, color=color, bold=bold, align=align, anchor='m')
    tf = slide.shapes[-1].text_frame
    tf.word_wrap = False
    bodyPr = tf._txBody.find(qn('a:bodyPr'))
    for tag in ('a:spAutoFit', 'a:normAutofit', 'a:noAutofit'):
        el = bodyPr.find(qn(tag))
        if el is not None:
            bodyPr.remove(el)
    bodyPr.append(bodyPr.makeelement(qn('a:noAutofit'), {}))
    for p in tf.paragraphs:
        pPr = p._p.get_or_add_pPr()
        lnSpc = pPr.makeelement(qn('a:lnSpc'), {})
        lnSpc.append(lnSpc.makeelement(qn('a:spcPct'), {'val': '100000'}))
        pPr.insert(0, lnSpc)
    return els


def chrome(slide, title=None, deck_title='', credit='', page=None, total=None, header=True, footer=True):
    """draw the template header bands, slide title and footer on a content slide.

    footer left half: short deck title (right-aligned, white); right half: `credit` on the left
    and 'page / total' on the right. `credit` names the SOURCE being discussed: its authors or
    institution and year (e.g. 'Ken Goldberg / UC Berkeley, 2026'), not the presenter; the
    presenter's name goes on the cover.
    Build steps of one concept pass the same `page`. Returns the title's elements."""
    T = TEMPLATE
    if header:
        for top, bot, col in T['header']:
            rect(slide, 0, top, _CANVAS_W, bot - top, fill=col, radius=0)
    els = []
    if title:
        t = T['title']
        els = text(slide, t['x'], t['y'], t['w'], t['h'], title, size=t['size'], color=t['color'], anchor='m')
    if footer:
        f = T['footer']
        y, h = f['top'], f['bottom'] - f['top']
        rect(slide, 0, y, f['split'], h, fill=f['left_fill'], radius=0)
        rect(slide, f['split'], y, _CANVAS_W - f['split'], h, fill=f['right_fill'], radius=0)
        band_text(slide, f['pad'], y, f['split'] - 2 * f['pad'], h, deck_title, f['size'], f['left_color'], align='r')
        band_text(slide, f['split'] + f['pad'], y, 1200, h, credit, f['size'], f['right_color'])
        if page is not None:
            num = f'{page} / {total}' if total else str(page)
            band_text(slide, _CANVAS_W - f['pad'] - 300, y, 300, h, num, f['size'], f['right_color'], align='r')
    return els


# ---------------------------------------------------------------------------
# Lists, videos and QR codes
# ---------------------------------------------------------------------------
def block(slide, x, y, w, h, title, items=None, size=30, radius=12):
    """titled block in the template's colours (TEMPLATE['block']), with optional bullet items."""
    B = TEMPLATE['block']
    th = B['title_h']
    els = rect(slide, x, y, w, th, fill=B['title_fill'], radius=radius)
    els += text(slide, x + 28, y, w - 56, th, title, size=B['size'], color=B['title_color'], bold=True, anchor='m')
    els += rect(slide, x, y + th, w, h - th, fill=B['body_fill'], radius=radius)
    if items:
        els += bullets(slide, x + 28, y + th + 30, w - 56, h - th - 50, items, size=size)
    return els


def bullets(slide, x, y, w, h, items, size=28, color=INK, char='•', indent=None, space_after=10):
    """bullet list with real paragraph bullets and a hanging indent.

    Do not type '•' into the text: its width differs between CJK and Latin runs and between
    renderers, so wrapped lines no longer align. items: str or [(text, style), ...] per line, as in `text`."""
    els = text(slide, x, y, w, h, items, size=size, color=color)
    tf = slide.shapes[-1].text_frame
    k = _font_scale(slide)
    ind = indent if indent is not None else size / 0.75 * 1.1   # px
    for p in tf.paragraphs:
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', str(int(_px(slide, ind))))
        pPr.set('indent', str(-int(_px(slide, ind))))
        for tag in ('a:buNone', 'a:buChar', 'a:buAutoNum', 'a:buFont', 'a:spcAft'):
            el = pPr.find(qn(tag))
            if el is not None:
                pPr.remove(el)
        spc = pPr.makeelement(qn('a:spcAft'), {})
        spc.append(spc.makeelement(qn('a:spcPts'), {'val': str(int(space_after * k * 100))}))
        pPr.append(spc)
        pPr.append(pPr.makeelement(qn('a:buFont'), {'typeface': LATIN_FONT}))
        pPr.append(pPr.makeelement(qn('a:buChar'), {'char': char}))
    return els


_VIDEO_MIME = {'.mp4': 'video/mp4', '.m4v': 'video/mp4', '.mov': 'video/quicktime', '.webm': 'video/webm',
               '.wmv': 'video/x-ms-wmv', '.avi': 'video/x-msvideo'}


def video(slide, path, x, y, w, h, poster=None, autoplay=True, loop=True, mute=True):
    """embed a video inside (x, y, w, h) keeping its aspect ratio (from the poster frame).

    poster: still image shown before playback and in renders (extract one with
    paper-project-setup's `asset_tools.py posters`). With autoplay=True every video on the slide
    starts together when the slide appears; loop=True repeats until the slide ends. Call it once per
    video; the slide's timing is rebuilt each time so several videos play in sync.
    returns (elements, box). Test playback in PowerPoint: LibreOffice renders only the poster."""
    import os
    box = (x, y, w, h)
    if poster:
        with Image.open(poster) as im:
            r = im.width / im.height
        if w / h > r:
            nw = h * r
            box = (x + (w - nw) / 2, y, nw, h)
        else:
            nh = w / r
            box = (x, y + (h - nh) / 2, w, nh)
    X, Y, W, H = box
    mime = _VIDEO_MIME.get(os.path.splitext(path)[1].lower(), 'video/mp4')
    mv = slide.shapes.add_movie(path, _px(slide, X), _px(slide, Y), _px(slide, W), _px(slide, H),
                                poster_frame_image=poster, mime_type=mime)
    el = mv._element
    spid = el.find('.//' + qn('p:cNvPr')).get('id')
    _VIDEOS.setdefault(id(slide._element), []).append((spid, autoplay, loop, mute))
    _video_timing(slide)
    return [el], box


_VIDEOS = {}   # slide element id -> [(shape id, autoplay, loop, mute)]


def _video_timing(slide):
    """(re)build <p:timing> so the slide's videos autoplay together and loop as flagged by `video`."""
    from lxml import etree
    P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    sld = slide._element
    vids = _VIDEOS.get(id(sld), [])
    old = sld.find(qn('p:timing'))
    if old is not None:
        sld.remove(old)
    if not vids:
        return
    n = [2]

    def nid():
        n[0] += 1
        return str(n[0])

    autos = [v for v in vids if v[1]]
    seq = ''
    if autos:                               # ids in document order: 2 = mainSeq, then the wrappers
        outer, inner = nid(), nid()
        calls = []
        for k, (i, _, _, _) in enumerate(autos):
            calls.append(
                f'<p:par><p:cTn id="{nid()}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" '
                f'nodeType="{"afterEffect" if k == 0 else "withEffect"}"><p:stCondLst><p:cond delay="0"/></p:stCondLst>'
                f'<p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="{nid()}" dur="indefinite" fill="hold"/>'
                f'<p:tgtEl><p:spTgt spid="{i}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par>')
        seq = (f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>'
               f'<p:par><p:cTn id="{outer}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
               f'<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst>'
               f'<p:par><p:cTn id="{inner}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
               + ''.join(calls) +
               '</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn>'
               '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
               '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>')
    media = []
    for i, _, lp, mu in vids:
        rep = ' repeatCount="indefinite"' if lp else ''
        mute = ' mute="1"' if mu else ''
        media.append(
            f'<p:video><p:cMediaNode vol="80000"{mute}><p:cTn id="{nid()}"{rep} fill="hold" display="0">'
            f'<p:stCondLst><p:cond delay="indefinite"/></p:stCondLst></p:cTn>'
            f'<p:tgtEl><p:spTgt spid="{i}"/></p:tgtEl></p:cMediaNode></p:video>')
    xml = (f'<p:timing xmlns:p="{P}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
           f'<p:childTnLst>{seq}{"".join(media)}</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>')
    timing = etree.fromstring(xml)
    ext = sld.find(qn('p:extLst'))
    if ext is not None:
        ext.addprevious(timing)
    else:
        sld.append(timing)


def qr(slide, data, x, y, size=300, label=None, label_size=22):
    """QR code for `data` (a URL or event link) at (x, y), size x size px, with an optional caption below.

    Uses `segno` (pure Python; install with `pip install segno`). If it is missing, or `data` is
    empty because the user has not given the link or event code yet, draws a labelled placeholder
    box instead; list every placeholder in the handoff so the user can fill it in."""
    import os
    import tempfile
    els = []
    try:
        if not data:
            raise ValueError('no data')
        import segno
        fd, png = tempfile.mkstemp(suffix='.png')
        os.close(fd)
        segno.make(data, error='m').save(png, scale=20, border=2)
        e, _ = picture(slide, png, x, y, size, size, alt=data)
        els += e
        os.remove(png)
    except Exception:
        els += rect(slide, x, y, size, size, fill='FFFFFF', line=MUTED, line_w=2, radius=8)
        els += text(slide, x, y, size, size, ['QR', 'placeholder'], size=24, color=MUTED, align='c', anchor='m')
    if label:
        lw = max(size + 80, text_width(label, label_size) + 24)
        els += text(slide, x + size / 2 - lw / 2, y + size + 10, lw, label_size / 0.75 * 1.4, label,
                    size=label_size, color=MUTED, align='c')
    return els

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


def _flat(line):
    """plain text of a line given as a string or as [(text, style), ...] runs."""
    return line if isinstance(line, str) else ''.join(t for t, _ in line)


def callout_size(lines, size=36, w=None):
    """(w, h) the callout box will have, so it can be positioned before it is drawn."""
    lh = size / 0.75 * 1.3
    padx, pady = 40, 26
    if w is None:
        w = max(text_width(_flat(l), size) for l in lines) + 2 * padx
    return w, lh * len(lines) + 2 * pady


def callout(slide, x, y, lines, size=36, w=None, align='c', anchor=None, valign='t', color=CALLRED):
    """bold callout whose box fits its text.
    color: red (default) when the callout IS the key point; INK or BLUE for a supporting remark,
    with only its key word in red: give such a line as runs, e.g. [('only ', {}), ('19.8%', {'color': CALLRED})].
    Red marks key points wherever they are; a slide with everything red has no key point.
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
    els += text(slide, x + padx * 0.5, y, w - padx, h, lines, size=size, color=color, bold=True, align=align, anchor='m')
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


def _draw_path(slide, pts, color=CALLRED, width=10):
    """a thin arrow along the points pts (px), arrowhead at the last point."""
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


def _quad(p0, c, p1, n=32):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]) for t in (i / n for i in range(n + 1))]


def _cubic(p0, c1, c2, p1, n=32):
    return [((1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * c1[0] + 3 * (1 - t) * t * t * c2[0] + t ** 3 * p1[0],
             (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * c1[1] + 3 * (1 - t) * t * t * c2[1] + t ** 3 * p1[1])
            for t in (i / n for i in range(n + 1))]


def arc_arrow(slide, p0, p1, bend=0.35, color=CALLRED, width=10, n=32):
    """curved red arrow from p0 to p1 (px), arrowhead at p1. bend > 0 bows to the left of the travel direction; ~0 is straight.
    The thin arrow: over a figure or on a slant (bend ~0 = straight). For a callout prefer annotate(),
    or curve_arrow() between two boxes: both make the curve leave one edge straight out and enter the
    callout straight in, which a symmetric bend from arc_arrow() does not."""
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    dx, dy = x1 - x0, y1 - y0
    cx, cy = mx - dy * bend, my + dx * bend
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append(((1 - t) ** 2 * x0 + 2 * (1 - t) * t * cx + t * t * x1,
                    (1 - t) ** 2 * y0 + 2 * (1 - t) * t * cy + t * t * y1))
    return _draw_path(slide, pts, color, width)


def block_arrow(slide, x, y, w, h, direction='down', fill=ARROWGRAY):
    """thick solid block arrow: straight, and only through free space, never lying on a picture or chart
    (use a thin arc_arrow there). For flow between pieces of content, or a lined-up callout (annotate()).
    direction names where the head points."""
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
    els[0].find('.//' + qn('p:cNvPr')).set('descr', 'hide')
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


def _covers(slide):
    """boxes of hide() covers: what lies under them is hidden, so a callout may sit there."""
    out = []
    for e in slide.shapes._spTree.iterchildren():
        nv = e.find('.//' + qn('p:cNvPr'))
        if nv is not None and nv.get('descr') == 'hide':
            b = box_of(e, slide)
            if b:
                out.append(b)
    return out


def _obstacles(slide, skip=()):
    """boxes of everything already on the slide's content area (header, title and footer excluded)."""
    out = []
    for e in slide.shapes._spTree.iterchildren():
        nv = e.find('.//' + qn('p:cNvPr'))
        if nv is not None and nv.get('descr') == 'hide':
            continue
        if e.tag not in (qn('p:sp'), qn('p:pic'), qn('p:cxnSp'), qn('p:grpSp'), qn('p:graphicFrame')):
            continue
        if id(e) in skip:
            continue
        b = box_of(e, slide)
        if not b or b[1] + b[3] <= CONTENT['y0'] or b[1] >= CONTENT['y1'] or b[2] >= 1900:
            continue
        out.append(b)
    return out


def _hits(b, obs, clear, covers=()):
    x, y, w, h = b
    for c in covers:                             # inside a hide() cover: nothing visible underneath
        if c[0] <= x and c[1] <= y and x + w <= c[0] + c[2] and y + h <= c[1] + c[3]:
            return False
    for o in obs:
        if x - clear < o[0] + o[2] and o[0] < x + w + clear and y - clear < o[1] + o[3] and o[1] < y + h + clear:
            return True
    return False


ARROW_MIN = 90      # px of visible arrow between the target and its callout


def _crossing(p0, p1, obs, n=40):
    """px of the straight path p0 -> p1 that runs over other content."""
    (x0, y0), (x1, y1) = p0, p1
    L = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
    hit = 0
    for i in range(1, n):
        t = i / n
        x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        if any(o[0] < x < o[0] + o[2] and o[1] < y < o[1] + o[3] for o in obs):
            hit += 1
    return L * hit / n



def _cross_pts(pts, obs):
    """px of the path through pts that runs over other content."""
    hit = 0.0
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        seg = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
        n = max(1, int(seg // 10))
        for i in range(n):
            t = (i + 0.5) / n
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            if any(o[0] < x < o[0] + o[2] and o[1] < y < o[1] + o[3] for o in obs):
                hit += seg / n
    return hit


CURVE_MIN = 60      # px a curved arrow needs along each axis to turn cleanly


def _routes(target, cbox, m=8):
    """curved paths from the middle of one target edge to the middle of one callout edge. Each leaves
    its edge straight out and enters the callout's edge straight in, so the bend is in the middle:
    'L' turns a quarter (right edge -> top of a callout below-right, bottom edge -> its left edge, ...);
    'S' keeps its direction (right edge -> left edge of a callout to the right but not lined up).
    Returns (axis of the exit 'h'/'v', 'L'/'S', points)."""
    tx, ty, tw, th = target
    cx, cy, cw, ch = cbox
    out = []
    for sx in (1, -1):                                   # out of the right / left edge
        S = (tx + tw + m if sx > 0 else tx - m, ty + th / 2)
        for sy in (1, -1):                               # into the top / bottom edge
            E = (cx + cw / 2, cy - m if sy > 0 else cy + ch + m)
            if (E[0] - S[0]) * sx >= CURVE_MIN and (E[1] - S[1]) * sy >= CURVE_MIN:
                out.append(('h', 'L', _quad(S, (E[0], S[1]), E)))
        E = (cx - m if sx > 0 else cx + cw + m, cy + ch / 2)
        if (E[0] - S[0]) * sx >= max(CURVE_MIN, 0.8 * abs(E[1] - S[1])):     # a squashed S reads as a kink
            k = (E[0] - S[0]) / 2
            out.append(('h', 'S', _cubic(S, (S[0] + k, S[1]), (E[0] - k, E[1]), E)))
    for sy in (1, -1):                                   # out of the bottom / top edge
        S = (tx + tw / 2, ty + th + m if sy > 0 else ty - m)
        for sx in (1, -1):                               # into the left / right edge
            E = (cx - m if sx > 0 else cx + cw + m, cy + ch / 2)
            if (E[0] - S[0]) * sx >= CURVE_MIN and (E[1] - S[1]) * sy >= CURVE_MIN:
                out.append(('v', 'L', _quad(S, (S[0], E[1]), E)))
        E = (cx + cw / 2, cy - m if sy > 0 else cy + ch + m)
        if (E[1] - S[1]) * sy >= max(CURVE_MIN, 0.8 * abs(E[0] - S[0])):
            k = (E[1] - S[1]) / 2
            out.append(('v', 'S', _cubic(S, (S[0], S[1] + k), (E[0], E[1] - k), E)))
    return out


def _path(target, cbox, side, lined, obs):
    """the thin arrow's points, how much of it runs over content, and whether it is clean.
    Lined up: straight between the facing edges. Otherwise the curve from _routes() that crosses the
    least content (quarter turns before S-bends, then the exit matching `side`, then the shortest);
    clean=False when none fits, and a plain bend is used (layout_check reports it as BEND)."""
    if lined:
        pts = list(_ends(target, cbox, side, True))
        return pts, _cross_pts(pts, obs), True
    want = 'h' if side in ('right', 'left') else 'v'
    best = None
    for ax, kind, pts in _routes(target, cbox):
        c = _cross_pts(pts, obs)
        L = sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for a, b in zip(pts, pts[1:]))
        sc = (round(c / 10), 0 if kind == 'L' else 1, 0 if ax == want else 1, L)
        if best is None or sc < best[0]:
            best = (sc, pts, c)
    if best:
        return best[1], best[2], True
    p0, p1 = _ends(target, cbox, side, False)
    bend = 0.3 if side in ('right', 'above') else -0.3
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    pts = _quad(p0, (mx - (p1[1] - p0[1]) * bend, my + (p1[0] - p0[0]) * bend), p1)
    return pts, _cross_pts(pts, obs), False


def curve_arrow(slide, src, dst, color=CALLRED, width=7):
    """a thin arrow from box src to box dst (px boxes, e.g. a frame and a callout you placed yourself).
    Straight between the facing edges when their centre lines meet (within 12 px); otherwise a curve
    that leaves the middle of one src edge straight out and enters one dst edge straight in, the turn
    in between (right edge -> top or bottom of a box off to the right, bottom edge -> its side, ...).
    Prefer annotate(), which also places the callout; use this when the layout is fixed by hand."""
    sx, sy, sw, sh = src
    dx, dy, dw, dh = dst
    if abs((sy + sh / 2) - (dy + dh / 2)) <= 12 or abs((sx + sw / 2) - (dx + dw / 2)) <= 12:
        horiz = abs((sy + sh / 2) - (dy + dh / 2)) <= 12
        side = ('right' if dx >= sx + sw else 'left') if horiz else ('below' if dy >= sy + sh else 'above')
        return _draw_path(slide, list(_ends(src, dst, side, True)), color, width)
    pts, _, clean = _path(src, dst, 'right', False, [])
    if not clean:
        _say(f'curve_arrow: no room for a clean curve between {src} and {dst}; move the boxes further apart')
    return _draw_path(slide, pts, color, width)

_SAID = set()


def _say(msg):
    """print a layout note once (build_steps redraws a slide once per step)."""
    if msg not in _SAID:
        _SAID.add(msg)
        print(msg)


THIN = {'grey': '8FA3B8', 'red': CALLRED}       # thin arrow colours (muted)
BLOCK = {'grey': ARROWGRAY, 'red': 'F3A6A6'}    # block arrow fills (muted)
_ARROW = {}                                     # slide or build -> (style, colour) fixed by its first callout


def annotate(slide, target, lines, side='right', style=None, color=None, size=36, frame_target=False,
             min_arrow=ARROW_MIN, clear=24, gap=None, outside=None, kind=None, text_color=CALLRED):
    """explain one thing with a callout: target -> arrow -> callout, drawn as ONE computed unit.

    target: (x, y, w, h) px of what is being explained (a bar, a point, part of a figure), taken
            from what picture(), hbars(), sub() or box_of() return, never estimated.
    side:   preferred side of the callout: 'right', 'below', 'left' or 'above'.
    style:  'block' = thick solid block arrow, only straight (callout lined up) and only through
            free space, never lying on a picture or chart; 'thin' = a line with an arrowhead,
            straight when lined up, curved when the callout is pulled out on a slant: the curve
            leaves the middle of one edge of the target straight out and enters one edge of the
            callout straight in (right edge -> top of a callout below-right, bottom edge -> its
            left edge), so the turn sits between them. A 'block'
            request falls back to 'thin' when no lined-up place with a clear path exists.
    color:  arrow colour, 'grey' (muted grey-blue) or 'red' (muted).
    text_color: the callout text colour: red when the callout is the key point, INK or BLUE for a
            supporting remark (then mark only its key word red with runs; see callout()).
    The first callout on a slide (or in one build_steps() slide) fixes style and colour; later
    calls keep them (a note is printed if they asked for something else), so the audience never
    sees the arrow change between steps. Leave style and color unset after the first call.
    Placement: the callout touches no other content (pictures, charts, text, shapes) with `clear`
    px around it (areas hidden with hide() count as free), at least `min_arrow` px from the target.
    Among free places: one that suits the style first, then the least arrow over other content,
    the preferred side, the nearest. When no free place exists, a warning is printed: shrink the
    figure, shorten the callout or move content.
    frame_target=True also draws a red frame around the target.
    gap / outside / kind: kept for older calls (a wanted distance; a box to avoid; 'therefore' =
    block grey, 'discuss' = thin red).
    Returns (elements, callout_box); give the elements to build_steps() as one part with box
    'remove', so frame, arrow and callout appear together and leave together."""
    if kind and not style:
        style, color = ('block', color or 'grey') if kind == 'therefore' else ('thin', color or 'red')
    key = _ARROW.get('build') or id(slide._element)
    fixed = _ARROW.get(key)
    want = (style or (fixed[0] if fixed else 'block'), color or (fixed[1] if fixed else 'grey'))
    if fixed and want != fixed:
        _say(f'annotate: {lines!r} asked for a {want[1]} {want[0]} arrow, but this slide uses {fixed[1]} '
              f'{fixed[0]}; kept {fixed[1]} {fixed[0]} (one arrow style per slide and its steps)')
        want = fixed
    style, color = want
    if gap is not None:
        min_arrow = max(min_arrow, gap)
    tx, ty, tw, th = target
    cw, ch = callout_size(lines, size)
    C = CONTENT
    covs = _covers(slide)
    inside_t = lambda o: o[0] >= tx - 2 and o[1] >= ty - 2 and o[0] + o[2] <= tx + tw + 2 and o[1] + o[3] <= ty + th + 2
    obs = [o for o in ([outside] if outside else []) + _obstacles(slide) if not inside_t(o)]
    holds = lambda o: o[0] <= tx and o[1] <= ty and o[0] + o[2] >= tx + tw and o[1] + o[3] >= ty + th
    path_obs = [o for o in obs if not holds(o)]
    figs = [o for o in obs if holds(o)]            # the picture or chart the target sits in
    gap0 = max(min_arrow, 150 if style == 'thin' else min_arrow) + 16
    best = None
    for sd in ('right', 'below', 'left', 'above'):
        for extra in range(0, 1000, 20):
            g = gap0 + extra
            if sd in ('below', 'above'):
                y = ty + th + g if sd == 'below' else ty - g - ch
                cands = [(tx + tw / 2 - cw / 2 + d, y) for d in range(-400, 401, 40)]
            else:
                x = tx + tw + g if sd == 'right' else tx - g - cw
                cands = [(x, ty + th / 2 - ch / 2 + d) for d in range(-300, 301, 20)]
            for cx, cy in cands:
                if cx < C['x0'] or cy < C['y0'] or cx + cw > C['x1'] or cy + ch > C['y1']:
                    continue
                if _hits((cx, cy, cw, ch), obs, clear, covs):
                    continue
                cb = (cx, cy, cw, ch)
                lap = (min(tx + tw, cx + cw) - max(tx, cx)) if sd in ('below', 'above') else \
                      (min(ty + th, cy + ch) - max(ty, cy))
                lined = lap >= min(60, (tw if sd in ('below', 'above') else th) - 2)
                p0, p1 = _ends(target, cb, sd, lined)
                block_ok = lined and _crossing(p0, p1, path_obs) == 0 and _crossing(p0, p1, figs) == 0
                _, cross, clean = _path(target, cb, sd, lined, path_obs)
                score = (0 if (style != 'block' or block_ok) else 1, 0 if clean else 1, round(cross / 10),
                         0 if sd == side else 1, g, -lap)
                if best is None or score < best[0]:
                    best = (score, sd, cx, cy, lined, block_ok)
            if best and best[0][:3] == (0, 0, 0) and extra > 200:
                break
    if best is None:
        sd = side
        cx = tx + tw + gap0 if sd == 'right' else tx - gap0 - cw if sd == 'left' else tx + tw / 2 - cw / 2
        cy = ty + th + gap0 if sd == 'below' else ty - gap0 - ch if sd == 'above' else ty + th / 2 - ch / 2
        cx = max(C['x0'], min(cx, C['x1'] - cw))
        cy = max(C['y0'], min(cy, C['y1'] - ch))
        _say(f'annotate: no free place for callout {lines!r}; shrink the figure, shorten the callout or move content')
        best = (None, sd, cx, cy, False, False)
    _, side, cx, cy, lined, block_ok = best
    if not fixed:
        _ARROW[key] = (style, color)
    els = []
    if frame_target:
        els += frame(slide, *target)
    cel, cbox = callout(slide, cx, cy, lines, size=size, color=text_color)
    p0, p1 = _ends(target, cbox, side, lined)
    if style == 'block' and block_ok:
        d = {'right': 'right', 'left': 'left', 'below': 'down', 'above': 'up'}[side]
        if side in ('right', 'left'):
            els += block_arrow(slide, min(p0[0], p1[0]), p0[1] - 30, abs(p1[0] - p0[0]), 60, d, fill=BLOCK[color])
        else:
            els += block_arrow(slide, p0[0] - 30, min(p0[1], p1[1]), 60, abs(p1[1] - p0[1]), d, fill=BLOCK[color])
    else:
        if style == 'block':
            _say(f'annotate: {lines!r}: a block arrow would lie on the figure or run on a slant here, so a thin '
                  f'arrow was drawn; use style=\'thin\' for this whole slide to keep its arrows alike')
        pts, _, clean = _path(target, cbox, side, lined, path_obs)
        if not clean:
            _say(f'annotate: {lines!r}: no room for a clean curve (straight out of one edge, straight into '
                  f'the callout); move the callout further out or line it up with what it explains')
        els += _draw_path(slide, pts, THIN[color], 7)
    els += cel
    for e in els:
        nv = e.find('.//' + qn('p:cNvPr'))
        if nv is not None:
            nv.set('descr', 'annotate')
    return els, cbox


def _ends(target, cbox, side, lined, m=8):
    """arrow start (on the target's edge) and end (on the callout's facing edge); a lined-up callout
    gets a straight path through the middle of the overlap."""
    tx, ty, tw, th = target
    cx, cy, cw, ch = cbox
    if side in ('below', 'above'):
        lo, hi = max(tx, cx), min(tx + tw, cx + cw)
        ax = (lo + hi) / 2 if (lined and hi > lo) else None
        y0, y1 = (ty + th + m, cy - m) if side == 'below' else (ty - m, cy + ch + m)
        return ((ax if ax is not None else tx + tw / 2), y0), ((ax if ax is not None else cx + cw / 2), y1)
    lo, hi = max(ty, cy), min(ty + th, cy + ch)
    ay = (lo + hi) / 2 if (lined and hi > lo) else None
    x0, x1 = (tx + tw + m, cx - m) if side == 'right' else (tx - m, cx + cw + m)
    return (x0, (ay if ay is not None else ty + th / 2)), (x1, (ay if ay is not None else cy + ch / 2))


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
    _ARROW['build'] = f'build{len(prs.slides._sldIdLst)}'   # one arrow style for all steps of this slide
    _ARROW.pop(_ARROW['build'], None)
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
                if box == 'auto':                # ONE mask over the part; outline-only shapes fade in place
                    filled = [e for e in els if e is not None and not _outline_only(e)]
                    dim([e for e in els if e is not None and _outline_only(e)], 25000)
                    b = bbox(filled, s, pad=6)
                    if b:
                        masks.append(b)
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
        merged = True                            # overlapping masks would stack into an opaque block
        while merged:
            merged = False
            for i in range(len(masks)):
                for j in range(i + 1, len(masks)):
                    a_, b_ = masks[i], masks[j]
                    if (a_[0] < b_[0] + b_[2] and b_[0] < a_[0] + a_[2] and a_[1] < b_[1] + b_[3] and b_[1] < a_[1] + a_[3]):
                        x0, y0 = min(a_[0], b_[0]), min(a_[1], b_[1])
                        x1 = max(a_[0] + a_[2], b_[0] + b_[2])
                        y1 = max(a_[1] + a_[3], b_[1] + b_[3])
                        masks[i] = (x0, y0, x1 - x0, y1 - y0)
                        del masks[j]
                        merged = True
                        break
                if merged:
                    break
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
    _ARROW.pop('build', None)
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

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
    """curved red arrow from p0 to p1 (px). bend > 0 bows to the left of the travel direction; ~0 is straight."""
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
    """solid block arrow for a direct 'this → so' link."""
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


def hide(slide, x, y, w, h, fill='FFFFFF', opacity=92000):
    """cover a part of an image that has NOT been explained yet (build by subtraction on a single image).

    This is the opposite of `dim`: `dim` fades what was already discussed, `hide` covers what is
    still to come. Prefer cropping or splitting the image into its parts when the parts are
    separable; use `hide` when they are not. Remove the cover on the step that explains that part."""
    els = rect(slide, x, y, w, h, fill=fill, radius=0)
    for c in els[0].iter(qn('a:srgbClr')):
        c.append(c.makeelement(qn('a:alpha'), {'val': str(opacity)}))
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

"""
Manim Design System — Reusable components for educational animations.
Usage: from design_system import *

Import into Manim scene files:
  import sys; sys.path.insert(0, '/path/to/references')
  from design_system import *
"""

from manim import *

# ── Design Tokens ──
class T:
    BG = "#0B1120"; PANEL = "#132040"; BORDER = "#1E3055"
    BLUE = "#4A9EFF"; GREEN = "#4ADE80"; RED = "#FF6B6B"
    YELLOW = "#FBBF24"; PURPLE = "#A78BFA"; ORANGE = "#F97316"
    WHITE = "#FFFFFF"; BODY = "#CBD5E1"; MUTED = "#64748B"
    FONT = "PingFang SC"
    H1 = 56; H2 = 36; H3 = 24; H4 = 20; BODY_S = 16; CAP = 13

FONT = T.FONT
Z = lambda s, **kw: Text(s, font=FONT, **kw)


def title_block(tag, tag_color, title, subtitle=""):
    """Tag + title + optional subtitle, top-aligned."""
    tw = max(len(tag) * 0.45 + 0.4, 1.2)
    tag_bg = RoundedRectangle(width=tw, height=0.45, corner_radius=0.22,
                              fill_color=tag_color, fill_opacity=1)
    tag_lbl = Z(tag, font_size=20, color=T.WHITE, weight=BOLD).move_to(tag_bg)
    tag_g = VGroup(tag_bg, tag_lbl).to_edge(UP, buff=0.6)
    t = Z(title, font_size=T.H1, color=T.WHITE, weight=BOLD).next_to(tag_g, DOWN, buff=0.5)
    g = VGroup(tag_g, t)
    if subtitle:
        s = Z(subtitle, font_size=26, color=T.BODY).next_to(t, DOWN, buff=0.3)
        g.add(s)
    return g


def info_card(icon, title, details, color, w=3.5, h=2.8):
    """Card with icon, title, bullet list."""
    bg = RoundedRectangle(width=w, height=h, corner_radius=0.3,
                          fill_color=T.PANEL, stroke_color=T.BORDER, stroke_width=1.5)
    ic = Z(icon, font_size=22, color=T.WHITE, weight=BOLD).next_to(bg, UP, buff=0.15)
    tl = Z(title, font_size=T.H3, color=color, weight=BOLD).next_to(ic, DOWN, buff=0.1)
    items = VGroup(*[Z(f"• {d}", font_size=T.BODY_S, color=T.MUTED) for d in details])
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(tl, DOWN, buff=0.15)
    return VGroup(bg, ic, tl, items)


def arch_layer(label, items, color, width=10):
    """Horizontal architecture layer."""
    box = RoundedRectangle(width=width, height=0.9, corner_radius=0.2,
                           fill_color=color, fill_opacity=0.12,
                           stroke_color=color, stroke_width=2)
    lbl = Z(label, font_size=22, color=color, weight=BOLD)
    det = Z(" · ".join(items), font_size=15, color=T.MUTED)
    return VGroup(lbl, box, det).arrange(RIGHT, buff=0.3)


def comparison_table(cols):
    """Side-by-side columns. cols: [(header, color, scope, [items])]"""
    columns = VGroup()
    for header, color, scope, items in cols:
        hb = RoundedRectangle(width=3.5, height=0.6, corner_radius=0.2,
                              fill_color=color, fill_opacity=0.2,
                              stroke_color=color, stroke_width=2)
        ht = Z(header, font_size=22, color=color, weight=BOLD).move_to(hb)
        sc = Z(scope, font_size=15, color=T.MUTED).next_to(hb, DOWN, buff=0.15)
        sep = Line(LEFT*1.5, RIGHT*1.5, color=T.BORDER, stroke_width=1).next_to(sc, DOWN, buff=0.15)
        il = VGroup(*[Z(f"• {i}", font_size=15, color=T.BODY) for i in items])
        il.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(sep, DOWN, buff=0.15)
        bg = RoundedRectangle(width=3.8, height=3.8, corner_radius=0.2,
                              fill_color=T.PANEL, fill_opacity=0.6,
                              stroke_color=T.BORDER, stroke_width=1)
        bg.move_to(VGroup(ht, sc, sep, il).get_center())
        columns.add(VGroup(bg, ht, sc, sep, il))
    return columns


def radial_graph(center, satellites, radius=2.8):
    """Star topology. satellites: [(label, color)]"""
    n = len(satellites)
    nodes, arrows = VGroup(), VGroup()
    for i, (label, color) in enumerate(satellites):
        a = (i / n) * TAU - PI / 2
        pos = np.array([radius * np.cos(a), radius * np.sin(a), 0])
        nd = Circle(radius=0.6, color=color, fill_opacity=0.08, stroke_width=1.5).move_to(pos)
        lb = Z(label, font_size=13, color=T.BODY, weight=BOLD)
        lb.move_to(pos + np.array([0.9*np.cos(a), 0.9*np.sin(a), 0]))
        nodes.add(VGroup(nd, lb))
        ar = Arrow(center, nd, buff=0.15, stroke_width=1.5, color=T.WHITE,
                   max_tip_length_to_length_ratio=0.15).set_opacity(0.2)
        arrows.add(ar)
    return VGroup(nodes, arrows)


def metric(label, value, unit="", color=T.WHITE, large=True):
    """Metric chip: label + number."""
    fs = 38 if large else 24
    lfs = 20 if large else 15
    bg = RoundedRectangle(width=2.5, height=1.4, corner_radius=0.2,
                          fill_color=T.PANEL, stroke_color=T.BORDER, stroke_width=1.5)
    l = Z(label, font_size=lfs, color=T.MUTED).next_to(bg, UP, buff=0.15)
    v = Z(value, font_size=fs, color=color, weight=BOLD).move_to(bg)
    if unit:
        u = Z(unit, font_size=15, color=T.MUTED).next_to(v, RIGHT, buff=0.1)
        v = VGroup(v, u)
    return VGroup(bg, l, v)

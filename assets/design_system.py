"""
Manim Design System — Reusable components for educational animations.
Single source of truth for ALL visual properties.

Usage:
    import sys; sys.path.insert(0, '<project-dir>')
    from design_system import *
"""

from manim import *


class T:
    """Design Tokens — do NOT hardcode values outside this class."""

    # ── Background ──
    BG = "#0B1120"
    BG_MEDIUM = "#132040"
    BG_LIGHT = "#1E3055"

    # ── Accent Colors (Kurzgesagt-inspired palette) ──
    BLUE = "#4A9EFF"
    GREEN = "#4ADE80"
    RED = "#FF6B6B"
    YELLOW = "#FBBF24"
    PURPLE = "#A78BFA"
    ORANGE = "#F97316"
    TEAL = "#00B8A9"
    ROSE = "#E94560"

    # ── Semantic Colors ──
    POSITIVE = "#00B894"
    NEGATIVE = "#E17055"
    NEUTRAL = "#74B9FF"

    # ── Text ──
    WHITE = "#FFFFFF"
    BODY = "#CBD5E1"
    MUTED = "#64748B"

    # ── Typography (1080p canvas) ──
    H1 = 56
    H2 = 36
    H3 = 24
    H4 = 20
    BODY_S = 16
    CAP = 13
    MIN_FONT = 13  # absolute minimum

    # ── Layout (Manim units, 14.22:8 aspect ratio) ──
    SAFE_TOP = 3.5
    SAFE_BOTTOM = -3.5
    SAFE_LEFT = -6.4
    SAFE_RIGHT = 6.4
    SUBTITLE_Y = -3.8

    # ── Font ──
    FONT = "PingFang SC"

    # ── Approved corner_radius for RoundedRectangle ──
    RADIUS = [0.05, 0.1, 0.2, 0.3, 0.5]

    # ── Approved stroke_width values ──
    STROKE = [1, 2, 3, 4]

    # ── Spacing scale (buff values for arrange/next_to) ──
    XS = 0.1
    SM = 0.2
    MD = 0.3
    LG = 0.5
    XL = 0.8


# ── Approved palette set (for style-scan.py validation) ──
APPROVED_HEX = set([
    T.BG, T.BG_MEDIUM, T.BG_LIGHT,
    T.BLUE, T.GREEN, T.RED, T.YELLOW, T.PURPLE, T.ORANGE, T.TEAL, T.ROSE,
    T.POSITIVE, T.NEGATIVE, T.NEUTRAL,
    T.WHITE, T.BODY, T.MUTED,
    "#000000", "#ffffff", "#fff", "#000",
])


def Z(s, **kw):
    """Text helper with default font."""
    defaults = {"font": T.FONT, "color": T.WHITE}
    defaults.update(kw)
    return Text(s, **defaults)


# ──────────────────────────────────────────────
# Reusable Components
# ──────────────────────────────────────────────

def title_block(tag, tag_color, title, subtitle=""):
    """Tag + title + optional subtitle, top-aligned."""
    tag_lbl = Z(tag, font_size=20, color=T.WHITE, weight=BOLD)
    tw = tag_lbl.width + 0.5
    tag_bg = RoundedRectangle(
        width=tw, height=0.45, corner_radius=0.22,
        fill_color=tag_color, fill_opacity=1
    )
    tag_lbl.move_to(tag_bg)
    tag_g = VGroup(tag_bg, tag_lbl).to_edge(UP, buff=0.6)
    t = Z(title, font_size=T.H1, color=T.WHITE, weight=BOLD).next_to(tag_g, DOWN, buff=T.SM)
    g = VGroup(tag_g, t)
    if subtitle:
        s = Z(subtitle, font_size=26, color=T.BODY).next_to(t, DOWN, buff=T.SM)
        g.add(s)
    return g


def info_card(icon_text, title_text, details, color, w=3.5, h=2.8):
    """Card with icon, title, bullet list."""
    bg = RoundedRectangle(
        width=w, height=h, corner_radius=0.3,
        fill_color=T.BG_MEDIUM, stroke_color=T.BG_LIGHT, stroke_width=1.5
    )
    ic = Z(icon_text, font_size=22, color=T.WHITE, weight=BOLD).next_to(bg, UP, buff=T.SM)
    tl = Z(title_text, font_size=T.H3, color=color, weight=BOLD).next_to(ic, DOWN, buff=T.XS)
    items = VGroup(*[Z(f"• {d}", font_size=T.BODY_S, color=T.MUTED) for d in details])
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(tl, DOWN, buff=T.SM)
    return VGroup(bg, ic, tl, items)


def arch_layer(label, items, color, width=10):
    """Horizontal architecture layer."""
    box = RoundedRectangle(
        width=width, height=0.9, corner_radius=0.2,
        fill_color=color, fill_opacity=0.12,
        stroke_color=color, stroke_width=2
    )
    lbl = Z(label, font_size=22, color=color, weight=BOLD)
    det = Z(" · ".join(items), font_size=15, color=T.MUTED)
    return VGroup(lbl, box, det).arrange(RIGHT, buff=T.MD)


def comparison_table(cols):
    """Side-by-side columns. cols: [(header, color, scope, [items])]"""
    columns = VGroup()
    for header, color, scope, items in cols:
        hb = RoundedRectangle(
            width=3.5, height=0.6, corner_radius=0.2,
            fill_color=color, fill_opacity=0.2,
            stroke_color=color, stroke_width=2
        )
        ht = Z(header, font_size=22, color=color, weight=BOLD).move_to(hb)
        sc = Z(scope, font_size=15, color=T.MUTED).next_to(hb, DOWN, buff=T.SM)
        sep = Line(LEFT * 1.5, RIGHT * 1.5, color=T.BG_LIGHT, stroke_width=1).next_to(sc, DOWN, buff=T.SM)
        il = VGroup(*[Z(f"• {i}", font_size=15, color=T.BODY) for i in items])
        il.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(sep, DOWN, buff=T.SM)
        bg_rect = RoundedRectangle(
            width=3.8, height=3.8, corner_radius=0.2,
            fill_color=T.BG_MEDIUM, fill_opacity=0.6,
            stroke_color=T.BG_LIGHT, stroke_width=1
        )
        bg_rect.move_to(VGroup(ht, sc, sep, il).get_center())
        columns.add(VGroup(bg_rect, ht, sc, sep, il))
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
        lb.move_to(pos + np.array([0.9 * np.cos(a), 0.9 * np.sin(a), 0]))
        nodes.add(VGroup(nd, lb))
        ar = Arrow(center, nd, buff=0.15, stroke_width=1.5, color=T.WHITE,
                   max_tip_length_to_length_ratio=0.15).set_opacity(0.2)
        arrows.add(ar)
    return VGroup(nodes, arrows)


def metric(label, value, unit="", color=T.WHITE, large=True):
    """Metric chip: label + number."""
    fs = 38 if large else 24
    lfs = 20 if large else 15
    bg = RoundedRectangle(
        width=2.5, height=1.4, corner_radius=0.2,
        fill_color=T.BG_MEDIUM, stroke_color=T.BG_LIGHT, stroke_width=1.5
    )
    l = Z(label, font_size=lfs, color=T.MUTED).next_to(bg, UP, buff=T.SM)
    v = Z(value, font_size=fs, color=color, weight=BOLD).move_to(bg)
    if unit:
        u = Z(unit, font_size=15, color=T.MUTED).next_to(v, RIGHT, buff=T.SM)
        v = VGroup(v, u)
    return VGroup(bg, l, v)


def subtitle_bar(text):
    """Bottom subtitle bar with semi-transparent background."""
    txt = Z(text, font_size=T.H3, color=T.WHITE)
    bg_rect = RoundedRectangle(
        width=txt.width + 0.8, height=0.55, corner_radius=0.27,
        fill_color=BLACK, fill_opacity=0.75
    )
    bg_rect.move_to(T.SUBTITLE_Y * UP)
    txt.move_to(bg_rect)
    return VGroup(bg_rect, txt)


def progressive_reveal(items, delay=0.5, animation_class=FadeIn, **anim_kwargs):
    """Return list of (animation, start_time) tuples for staggered reveal."""
    result = []
    for i, item in enumerate(items):
        start_time = i * delay
        result.append((animation_class(item, **anim_kwargs), start_time))
    return result


def focus_highlight(mobject, color=None):
    """Add a glowing highlight background behind a mobject."""
    if color is None:
        color = T.BLUE
    rect = SurroundingRectangle(
        mobject, color=color, fill_opacity=0.08,
        stroke_width=2, buff=0.15
    )
    return VGroup(rect, mobject)


def staggered_animation(mobjects, animation_class=FadeIn, lag_ratio=0.3, **kwargs):
    """Play animation on a group with staggered timing."""
    return animation_class(VGroup(*mobjects), lag_ratio=lag_ratio, **kwargs)


def annotate_arrow(start, end, label="", color=None):
    """Arrow with optional label between two points or mobjects."""
    if color is None:
        color = T.WHITE
    ar = Arrow(start, end, stroke_width=2, color=color,
               max_tip_length_to_length_ratio=0.15, buff=0.1)
    if label:
        mid = (np.array(start) + np.array(end)) / 2
        lbl = Z(label, font_size=T.CAP, color=T.BODY).next_to(mid, UP, buff=T.SM)
        return VGroup(ar, lbl)
    return ar


def scene_bg(color=None):
    """Set scene background color."""
    return {
        "camera": {"background_color": color or T.BG}
    }


def accent_bg(scene, color=None):
    """Apply background with subtle radial gradient effect."""
    c = color or T.BG
    # Manim doesn't support CSS gradients; use layered rects for depth
    bg1 = Rectangle(
        width=14.22, height=8, fill_color=c, fill_opacity=1
    )
    bg2 = Rectangle(
        width=14.22, height=8, fill_color=color or T.BG_MEDIUM,
        fill_opacity=0.3
    )
    return VGroup(bg1, bg2)

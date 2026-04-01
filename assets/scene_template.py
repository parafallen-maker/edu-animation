"""
Scene Template — Standard educational video scene structure.

Copy and customize for each scene. Layout zones (Manim coordinates):
  - Title Zone: y > 2.5
  - Content Zone: y ∈ [-1.0, 2.5]
  - Info Cards Zone: y ∈ [-2.5, -1.0]
  - Subtitle Zone: y < -3.2

Usage:
    import sys; sys.path.insert(0, '.')
    from design_system import *
"""

from manim import *


class SceneTemplate(Scene):
    """
    Standard scene template with proper layout zones.

    Modify the construct() method for your content.
    Each scene should last as long as its narration audio.
    """

    def setup(self):
        """Configure camera background."""
        self.camera.background_color = T.BG

    def construct(self):
        # ─── Title Section (y > 2.5) ───
        title = Z("Scene Title", font_size=T.H1, color=T.WHITE, weight=BOLD)
        title.move_to(UP * 3 + LEFT * 0.5)

        tag = Z("TAG", font_size=20, color=T.WHITE, weight=BOLD)
        tag_bg = RoundedRectangle(
            width=tag.width + 0.5, height=0.4, corner_radius=0.2,
            fill_color=T.BLUE, fill_opacity=1
        )
        tag.move_to(tag_bg)
        tag_g = VGroup(tag_bg, tag).next_to(title, UP, buff=T.SM)

        title_group = VGroup(tag_g, title)

        # ─── Content Zone (y ∈ [-1.0, 2.5]) ───
        # Place your main diagrams, illustrations here
        content = VGroup(
            Circle(radius=1.5, color=T.BLUE, fill_opacity=0.1, stroke_width=2),
            Z("Content Here", font_size=T.H3, color=T.BODY),
        ).arrange(DOWN, buff=T.MD)

        # ─── Subtitle Zone (y < -3.2) ───
        subtitle = subtitle_bar("Narration text appears here")

        # ─── Animation Sequence ───
        # Phase 1: Title entrance (~1s)
        self.play(
            FadeIn(tag_g, shift=DOWN * 0.2),
            FadeIn(title, shift=DOWN * 0.2),
            run_time=0.8,
        )

        # Phase 2: Content entrance (~2s)
        self.play(
            FadeIn(content, scale=0.95),
            run_time=1.0,
        )

        # Phase 3: Subtitle entrance
        self.play(FadeIn(subtitle, shift=UP * 0.1), run_time=0.5)

        # Phase 4: Hold for narration
        # >>> Set this to: audio_duration - (animation_budget)
        # >>> e.g., audio=10s, animation_budget=3.5s → wait(6.5)
        self.wait(5.0)

        # Phase 5: Exit (~0.5s)
        self.play(
            FadeOut(title_group),
            FadeOut(content),
            FadeOut(subtitle),
            run_time=0.5,
        )


# ──────────────────────────────────────────────
# Timing Reference
# ──────────────────────────────────────────────
# Chinese narration: ~4 chars/sec
# → 60-char narration ≈ 15s scene
# Animation budget: use 2-4s for entrance animations
# Remaining time: self.wait() to fill audio duration
#
# Common run_time values:
#   Micro (badge/toggle):  0.1-0.2s
#   Fast (icon entrance):  0.3-0.5s
#   Normal (card/panel):   0.5-0.8s
#   Slow (full-screen):    1.0-1.5s
#   Dramatic (transition): 1.5-2.5s

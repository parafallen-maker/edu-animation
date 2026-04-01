"""
天空为什么是蓝色的 — 60 秒通识科普 Manim 视频
核心隐喻：弹球台（大气分子=钉子，蓝光=小弹球被弹开，红光=大弹球穿过）
"""
from manim import *
import json
import os
import random

from config import COLORS, RAINBOW, FONT

random.seed(42)

# 加载时间线
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "audio", "narration")
with open(os.path.join(AUDIO_DIR, "timeline.json"), "r") as f:
    TL = json.load(f)


def audio_path(seg_id: str) -> str:
    return TL[seg_id]["path"]


def dur(seg_id: str) -> float:
    return TL[seg_id]["duration"]


class WhySkyIsBlue(MovingCameraScene):

    def construct(self):
        self.camera.background_color = COLORS["bg"]
        self.do_hook()
        self.do_setup()
        self.do_core()
        self.do_aha()
        self.do_ending()

    # ==================== HOOK (≈5s) ====================
    def do_hook(self):
        # "天空为什么是蓝色的？"
        q = Text("天空为什么是蓝色的？", font=FONT,
                  font_size=56, color=COLORS["blue_light"])
        self.add_sound(audio_path("hook_1"))
        self.play(Write(q), run_time=1.6)
        self.wait(dur("hook_1") - 1.6)

        # "不是因为大海的倒影。"
        self.add_sound(audio_path("hook_2"))
        cross = Cross(q, stroke_color=COLORS["red_light"], stroke_width=6)
        self.play(Create(cross), run_time=0.6)
        self.wait(dur("hook_2") - 0.6)

        self.play(FadeOut(q), FadeOut(cross), run_time=0.4)

    # ==================== SETUP (≈6s) ====================
    def do_setup(self):
        # 太阳 + 白光
        sun = Circle(radius=0.6, color=COLORS["sun_yellow"],
                     fill_opacity=1, stroke_width=0)
        sun_glow = Circle(radius=0.9, color=COLORS["sun_yellow"],
                          fill_opacity=0.15, stroke_width=0)
        sun_group = VGroup(sun_glow, sun).to_edge(LEFT, buff=1)

        white_ray = Line(
            sun.get_right() + RIGHT * 0.1, RIGHT * 1,
            color=COLORS["white"], stroke_width=8
        )

        self.add_sound(audio_path("setup_1"))
        self.play(FadeIn(sun_group), run_time=0.6)
        self.play(Create(white_ray), run_time=0.8)
        self.wait(dur("setup_1") - 1.4)

        # 白光分成彩虹
        prism = Triangle(color=COLORS["white"], fill_opacity=0.12,
                         stroke_width=2, stroke_color=COLORS["gray"])
        prism.scale(0.7).move_to(RIGHT * 1)

        spread_angles = [0.5, 0.3, 0.1, -0.1, -0.3, -0.5]
        rainbow_rays = VGroup(*[
            Line(prism.get_right(), prism.get_right() + RIGHT * 4.5
                 + UP * a * 2.5,
                 color=c, stroke_width=5)
            for c, a in zip(RAINBOW, spread_angles)
        ])

        self.add_sound(audio_path("setup_2"))
        self.play(FadeIn(prism), run_time=0.4)
        self.play(
            ReplacementTransform(white_ray, rainbow_rays),
            run_time=1.2
        )
        self.wait(dur("setup_2") - 1.6)

        # 清场
        self.play(
            FadeOut(sun_group), FadeOut(prism), FadeOut(rainbow_rays),
            run_time=0.5
        )

    # ==================== CORE — 弹球台隐喻 (≈22s) ====================
    def do_core(self):
        # --- 构建弹球台 ---
        # "现在想象一下，大气层是一个巨大的弹球台。"
        title = Text("大气层 ≈ 弹球台", font=FONT,
                      font_size=40, color=COLORS["white"])
        title.to_edge(UP, buff=0.4)

        self.add_sound(audio_path("core_1"))
        self.play(Write(title), run_time=1.2)
        self.wait(dur("core_1") - 1.2)

        # "空气中的分子，就是上面密密麻麻的小钉子。"
        pins = VGroup(*[
            Dot(
                point=[random.uniform(-5.5, 5.5), random.uniform(-2.5, 2), 0],
                radius=0.055, color=COLORS["particle"]
            )
            for _ in range(100)
        ])

        self.add_sound(audio_path("core_2"))
        self.play(
            LaggedStart(*[FadeIn(p, scale=0.5) for p in pins], lag_ratio=0.015),
            run_time=2.0
        )
        self.wait(dur("core_2") - 2.0)

        # --- 蓝光小弹球 ---
        # "蓝光的波长短，就像一个小弹球。碰到钉子就被弹得到处都是。"
        blue_label = Text("蓝光 = 小弹球", font=FONT,
                          font_size=28, color=COLORS["blue_light"])
        blue_label.to_edge(DOWN, buff=0.4)

        blue_ball = Dot(color=COLORS["blue_light"], radius=0.15)
        blue_ball.move_to(LEFT * 7 + UP * 0.5)

        zigzag = [
            LEFT * 7 + UP * 0.5,
            LEFT * 4.5 + UP * 1.8,
            LEFT * 2.5 + DOWN * 0.8,
            LEFT * 0.5 + UP * 1.5,
            RIGHT * 1.5 + DOWN * 1.2,
            RIGHT * 0.5 + UP * 2.2,
            RIGHT * 3 + DOWN * 0.3,
            RIGHT * 2 + UP * 1,
        ]
        blue_path = VMobject()
        blue_path.set_points_smoothly([np.array(p) for p in zigzag])

        scatter_dots = VGroup(*[
            Dot(point=p, radius=0.08, color=COLORS["blue_light"],
                fill_opacity=0.35)
            for p in zigzag[1:]
        ])

        self.add_sound(audio_path("core_3"))
        self.play(Write(blue_label), run_time=0.5)
        self.play(MoveAlongPath(blue_ball, blue_path), run_time=4.5,
                  rate_func=linear)
        self.play(FadeIn(scatter_dots), run_time=0.3)
        self.wait(dur("core_3") - 5.3)

        # --- 红光大弹球 ---
        # "而红光的波长长，就像一个大弹球。钉子根本挡不住它，直接穿过去了。"
        red_label = Text("红光 = 大弹球", font=FONT,
                         font_size=28, color=COLORS["red_light"])
        red_label.next_to(blue_label, UP, buff=0.3)

        red_ball = Dot(color=COLORS["red_light"], radius=0.25)
        red_ball.move_to(LEFT * 7 + DOWN * 0.5)

        straight_path = Line(LEFT * 7 + DOWN * 0.5, RIGHT * 7 + DOWN * 0.5)

        self.add_sound(audio_path("core_4"))
        self.play(
            FadeOut(blue_ball),
            Write(red_label),
            run_time=0.6
        )
        self.play(
            MoveAlongPath(red_ball, straight_path),
            run_time=3,
            rate_func=linear
        )
        self.wait(dur("core_4") - 3.6)

        # 清场
        self.play(
            FadeOut(title), FadeOut(pins), FadeOut(scatter_dots),
            FadeOut(blue_label), FadeOut(red_label), FadeOut(red_ball),
            run_time=0.6
        )

    # ==================== AHA MOMENT (≈6s) ====================
    def do_aha(self):
        # "所以你抬头看到的蓝色"
        self.add_sound(audio_path("aha_1"))

        person = VGroup(
            Circle(radius=0.2, color=COLORS["white"], fill_opacity=1,
                   stroke_width=0),
            Line(ORIGIN, DOWN * 0.6, color=COLORS["white"], stroke_width=3),
            Line(DOWN * 0.6, DOWN * 0.6 + DL * 0.4, color=COLORS["white"],
                 stroke_width=3),
            Line(DOWN * 0.6, DOWN * 0.6 + DR * 0.4, color=COLORS["white"],
                 stroke_width=3),
        ).move_to(DOWN * 2)

        up_arrow = Arrow(
            person[0].get_top(), person[0].get_top() + UP * 1.5,
            color=COLORS["blue_light"], stroke_width=3, buff=0.1
        )

        self.play(FadeIn(person), run_time=0.5)
        self.play(GrowArrow(up_arrow), run_time=0.6)
        self.wait(dur("aha_1") - 1.1)

        # "就是被弹得满天都是的蓝光"
        self.add_sound(audio_path("aha_2"))

        blue_dots = VGroup(*[
            Dot(
                point=[random.uniform(-6, 6), random.uniform(0, 3.5), 0],
                radius=random.uniform(0.04, 0.12),
                color=COLORS["blue_light"],
                fill_opacity=random.uniform(0.2, 0.7)
            )
            for _ in range(120)
        ])

        sky_rect = Rectangle(
            width=15, height=4.5, fill_opacity=0.25,
            fill_color=COLORS["blue_light"], stroke_width=0
        ).move_to(UP * 1.5)

        self.play(
            FadeIn(sky_rect),
            LaggedStart(*[FadeIn(d, scale=0.3) for d in blue_dots],
                        lag_ratio=0.008),
            run_time=2.0
        )
        self.wait(dur("aha_2") - 2.0)

        # 汇聚为蓝色天空 — 所有散射蓝点 opacity 拉满
        self.play(
            sky_rect.animate.set_fill(opacity=0.6),
            *[d.animate.set_fill(opacity=0.8) for d in blue_dots[:40]],
            run_time=1.0
        )

        self.play(
            FadeOut(person), FadeOut(up_arrow),
            FadeOut(blue_dots), FadeOut(sky_rect),
            run_time=0.5
        )

    # ==================== ENDING 余韵 (≈4s) ====================
    def do_ending(self):
        # "天空的颜色，是光的弹球游戏。"
        self.add_sound(audio_path("ending"))

        ending = Text("天空的颜色\n是光的弹球游戏", font=FONT,
                       font_size=52, color=COLORS["blue_light"],
                       line_spacing=1.2)
        self.play(FadeIn(ending, shift=UP * 0.3), run_time=1.5)
        self.wait(dur("ending") - 1.5)
        self.play(FadeOut(ending), run_time=1.0)
        self.wait(0.5)

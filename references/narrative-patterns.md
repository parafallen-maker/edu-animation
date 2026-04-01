# Narrative Animation Patterns

One level above component animations (FadeIn, Scale). Each pattern = **a complete storytelling action**.

## When to Use

In Phase 2 (Visual Narrative Design), assign one pattern to each section of the storyboard. These patterns tell the LLM *how* to structure scene-level animation, not just which Manim primitives to call.

---

## Pattern 1: Build Up and Reveal (铺垫揭示)

**Purpose:** Show parts individually, then reveal they form a whole.

**Use for:** System composition, "guess what this is", surprising connections.

**Example:** Show wings, engine, fuselage separately → zoom out → it's an airplane.

```python
def build_up_and_reveal(scene, parts, labels, whole, whole_label):
    """
    parts: list[Mobject] — individual components
    labels: list[str] — label for each part
    whole: Mobject — the assembled result
    whole_label: str — label for the whole
    """
    label_mobjects = []
    for part, label in zip(parts, labels):
        text = Z(label, font_size=T.H4, color=T.BODY)
        text.next_to(part, DOWN, buff=T.SM)
        scene.play(FadeIn(part, shift=UP * 0.3), Write(text), run_time=0.8)
        scene.wait(0.5)
        label_mobjects.append(text)

    # Converge
    scene.play(
        *[p.animate.move_to(whole.get_center()) for p in parts],
        *[FadeOut(t) for t in label_mobjects],
        run_time=1.5, rate_func=smooth
    )
    # Reveal
    wl = Z(whole_label, font_size=T.H2, color=T.WHITE, weight=BOLD)
    wl.next_to(whole, DOWN, buff=T.MD)
    scene.play(
        FadeOut(VGroup(*parts)),
        FadeIn(whole, scale=1.2),
        Write(wl),
        run_time=1
    )
    return VGroup(whole, wl)
```

---

## Pattern 2: Cause and Effect Chain (因果链)

**Purpose:** A causes B, B causes C. Visualize cascading causation.

**Use for:** Mechanisms, chain reactions, cascading failures, explanations of "why".

**Example:** Greenhouse gas ↑ → Temperature ↑ → Ice melts → Sea level ↑

```python
def cause_and_effect(scene, nodes, node_labels, direction=RIGHT):
    """
    nodes: list[Mobject] — visual for each step
    node_labels: list[str] — text label for each step
    direction: arrangement direction
    """
    prev = None
    all_elements = VGroup()
    for node, label in zip(nodes, node_labels):
        text = Z(label, font_size=T.H4, color=T.BODY)
        text.next_to(node, DOWN, buff=T.SM)
        scene.play(GrowFromCenter(node), Write(text), run_time=0.6)
        if prev is not None:
            arrow = Arrow(prev.get_right(), node.get_left(),
                          buff=0.2, color=T.YELLOW, stroke_width=2)
            scene.play(GrowArrow(arrow), run_time=0.4)
            all_elements.add(arrow)
        prev = node
        all_elements.add(node, text)
        scene.wait(0.3)
    return all_elements
```

---

## Pattern 3: Compare and Contrast (左右对比)

**Purpose:** Side-by-side comparison of two things.

**Use for:** Old vs. new, correct vs. incorrect, before vs. after, option A vs. B.

**Example:** Traditional car vs. electric car, blue light vs. red light.

```python
def compare_and_contrast(scene, left, right, left_label, right_label,
                         divider_color=None):
    """
    left, right: Mobject — the two things to compare
    """
    if divider_color is None:
        divider_color = T.MUTED
    line = Line(UP * 3, DOWN * 3, color=divider_color, stroke_width=1.5)
    lt = Z(left_label, font_size=T.H3, color=T.BLUE, weight=BOLD)
    rt = Z(right_label, font_size=T.H3, color=T.RED, weight=BOLD)

    left_group = VGroup(lt, left).arrange(DOWN, buff=T.MD).move_to(LEFT * 3.5)
    right_group = VGroup(rt, right).arrange(DOWN, buff=T.MD).move_to(RIGHT * 3.5)

    scene.play(Create(line), run_time=0.5)
    scene.play(
        FadeIn(left_group, shift=LEFT * 0.3),
        FadeIn(right_group, shift=RIGHT * 0.3),
        run_time=1
    )
    return VGroup(line, left_group, right_group)
```

---

## Pattern 4: Zoom Into Detail (聚焦放大)

**Purpose:** From overview to detail. Show the big picture, then magnify a specific part.

**Use for:** Microscopic structures, zooming into mechanisms, focusing on key components.

**Example:** A tree → zoom into leaf → zoom into chloroplast → photosynthesis.

**Requires:** `MovingCameraScene`

```python
def zoom_into_detail(scene, overview, detail, zoom_target_pos,
                     zoom_width=4, label_text=""):
    """
    overview: Mobject — the full picture
    detail: Mobject — what appears after zooming in
    zoom_target_pos: np.array — center of zoom
    """
    scene.play(FadeIn(overview), run_time=1)
    scene.wait(0.5)

    # Focus indicator
    circle = Circle(radius=0.5, color=T.YELLOW, stroke_width=3)
    circle.move_to(zoom_target_pos)
    scene.play(Create(circle), run_time=0.5)

    # Zoom
    scene.play(
        scene.camera.frame.animate.set(width=zoom_width).move_to(zoom_target_pos),
        FadeOut(circle),
        run_time=1.5, rate_func=smooth
    )
    scene.play(FadeIn(detail), run_time=0.8)

    if label_text:
        lbl = Z(label_text, font_size=T.H4, color=T.WHITE)
        lbl.next_to(detail, DOWN, buff=T.SM)
        scene.play(Write(lbl), run_time=0.5)
```

---

## Pattern 5: Before and After (前后对比)

**Purpose:** Show transformation/change over time.

**Use for:** Impact visualization, evolution, process results.

**Example:** Pre-industrial city → post-industrial city.

```python
def before_and_after(scene, before, after,
                     before_label="之前", after_label="之后",
                     use_transform=True):
    """
    before, after: Mobject — the two states
    use_transform: if True, morph between states; if False, wipe transition
    """
    bl = Z(before_label, font_size=T.H4, color=T.MUTED)
    bl.to_edge(UP, buff=0.5)
    scene.play(FadeIn(before), Write(bl), run_time=1)
    scene.wait(1)

    al = Z(after_label, font_size=T.H4, color=T.MUTED)
    al.to_edge(UP, buff=0.5)

    if use_transform:
        scene.play(
            Transform(before, after),
            Transform(bl, al),
            run_time=2, rate_func=smooth
        )
    else:
        scene.play(FadeOut(before, shift=LEFT), FadeOut(bl), run_time=0.5)
        scene.play(FadeIn(after, shift=RIGHT), Write(al), run_time=0.5)
```

---

## Pattern 6: Misconception Correction (错误纠正)

**Purpose:** Show a common misconception, cross it out, then show the truth.

**Use for:** Addressing wrong intuitions, debunking myths.

**Example:** "Heavier objects fall faster" ✗ → "All objects fall at the same rate in vacuum" ✓

```python
def misconception_correction(scene, wrong_text, right_text, proof_mobject=None):
    """
    wrong_text: str — the misconception
    right_text: str — the correct understanding
    proof_mobject: Mobject — optional visual proof
    """
    wrong = Z(wrong_text, font_size=T.H3, color=T.RED)
    scene.play(Write(wrong), run_time=1)
    scene.wait(1)

    cross = Cross(wrong, stroke_color=T.RED, stroke_width=5)
    scene.play(Create(cross), run_time=0.6)
    scene.wait(0.5)

    right = Z(right_text, font_size=T.H3, color=T.GREEN)
    right.next_to(wrong, DOWN, buff=T.LG)
    scene.play(Write(right), run_time=1)

    if proof_mobject:
        proof_mobject.next_to(right, DOWN, buff=T.MD)
        scene.play(FadeIn(proof_mobject), run_time=1)
```

---

## Pattern 7: Progressive Reveal (渐进揭示)

**Purpose:** Incrementally add complexity to the same visual. Each step builds on the previous.

**Use for:** Formulas, diagrams that grow, layered explanations.

**Example:** F=ma → F=m(dv/dt) → F⃗=m(dv⃗/dt)

```python
def progressive_reveal(scene, stages, stage_labels=None, pause_between=1.0):
    """
    stages: list[Mobject] — each stage replaces the previous
    stage_labels: list[str] — optional label per stage
    """
    current = stages[0]
    scene.play(Write(current), run_time=1)
    if stage_labels:
        lbl = Z(stage_labels[0], font_size=T.H4, color=T.MUTED)
        lbl.to_edge(DOWN)
        scene.play(FadeIn(lbl), run_time=0.3)
    scene.wait(pause_between)

    for i, stage in enumerate(stages[1:], 1):
        if stage_labels and i < len(stage_labels):
            new_lbl = Z(stage_labels[i], font_size=T.H4, color=T.MUTED)
            new_lbl.to_edge(DOWN)
            scene.play(Transform(lbl, new_lbl), run_time=0.3)
        scene.play(Transform(current, stage), run_time=1.5)
        scene.wait(pause_between)
```

---

## Choosing the Right Pattern

| You want to show... | Pattern |
|---|---|
| Parts → Whole | Build Up and Reveal |
| A causes B causes C | Cause and Effect |
| X vs. Y side by side | Compare and Contrast |
| Big picture → close-up | Zoom Into Detail |
| State change over time | Before and After |
| "Actually, that's wrong..." | Misconception Correction |
| Simple → Complex evolution | Progressive Reveal |

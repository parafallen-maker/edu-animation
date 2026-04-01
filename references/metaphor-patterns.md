# Visual Metaphor Patterns

A popscience video lives or dies by its core metaphor. This library provides reusable metaphor patterns — select or combine them in **Phase 1.5: Core Metaphor Design**.

## How to Use

For each key concept in your script:
1. Identify the abstract mechanism (e.g., "data flows between servers")
2. Find the best matching pattern below
3. Fill in the mapping table: source domain → target domain
4. Note where the analogy breaks down → address in narration

## Pattern Library

### Flow Analogy (流动类比)

**Suitable for:** electric current, information transmission, logistics, blood circulation, economic flows, data pipelines

**Visual:** Pipes/channels + moving particles

**Variable mapping:**
- Flow speed = intensity/strength
- Pipe diameter = channel capacity
- Branching = distribution/routing
- Blockage = bottleneck

**Manim recipe:**
```python
# Particles flowing along a curved path
path = CubicBezier(start, ctrl1, ctrl2, end)
particles = VGroup(*[Dot(radius=0.06, color=T.BLUE) for _ in range(20)])
for i, p in enumerate(particles):
    self.play(MoveAlongPath(p, path),
              run_time=2, rate_func=linear,
              lag_ratio=0.1)
```

---

### Container Analogy (容器类比)

**Suitable for:** memory, budget, energy conservation, capacity limits, resource pools

**Visual:** Glass/tank + liquid level change

**Variable mapping:**
- Water level = current amount
- Container size = upper limit
- Overflow = crash/failure
- Drain = consumption

**Manim recipe:**
```python
# Tank with animated water level
tank = Rectangle(width=2, height=3, color=T.WHITE, stroke_width=2)
water = Rectangle(width=1.9, height=0, fill_color=T.BLUE, fill_opacity=0.6)
water.align_to(tank, DOWN).shift(UP * 0.05)
self.play(water.animate.stretch_to_fit_height(2), run_time=2)
```

---

### Tree / Hierarchy Analogy (层级/树形类比)

**Suitable for:** organizational structure, taxonomy, decision trees, evolution, file systems

**Visual:** Root growing into branches

**Variable mapping:**
- Node = entity
- Edge = relationship
- Depth = hierarchy level
- Leaf = terminal/result

**Manim recipe:**
```python
# Growing tree with LaggedStart
graph = Graph(vertices, edges, layout="tree")
self.play(LaggedStart(*[GrowFromPoint(v, graph.vertices[0].get_center())
          for v in graph.vertices.values()], lag_ratio=0.3))
```

---

### Balance / Scale Analogy (天平/对比类比)

**Suitable for:** trade-offs, supply-demand, pros-cons, equilibrium

**Visual:** Seesaw/scale with weights on both sides

**Variable mapping:**
- Left side = option A
- Right side = option B
- Tilt angle = advantage/disadvantage
- Weight = importance

**Manim recipe:**
```python
# Seesaw that tilts
fulcrum = Triangle(color=T.WHITE, fill_opacity=0.3).scale(0.3).to_edge(DOWN)
beam = Line(LEFT * 3, RIGHT * 3, color=T.WHITE, stroke_width=4)
beam.move_to(fulcrum.get_top())
# Rotate beam to show imbalance
self.play(Rotate(beam, angle=-15 * DEGREES, about_point=fulcrum.get_top()))
```

---

### Chain Reaction Analogy (链式反应类比)

**Suitable for:** cause-effect chains, butterfly effect, domino effect, cascade propagation

**Visual:** Dominoes falling sequentially / gears meshing

**Variable mapping:**
- Each domino = one step in the chain
- Falling = triggering
- Spacing = time delay
- Last domino = final consequence

**Manim recipe:**
```python
# Domino chain with LaggedStart
dominoes = VGroup(*[
    Rectangle(width=0.15, height=0.8, fill_color=T.WHITE, fill_opacity=0.8)
    .shift(RIGHT * i * 0.5) for i in range(10)
])
# Each domino rotates to "fall"
self.play(LaggedStart(*[
    Rotate(d, angle=-80*DEGREES, about_point=d.get_bottom())
    for d in dominoes
], lag_ratio=0.15), run_time=3)
```

---

### Scale / Zoom Analogy (缩放类比)

**Suitable for:** micro/macro perspective shifts, scale comparisons, proportional reasoning

**Visual:** Zoom in/out from one object to another scale

**Variable mapping:**
- Zoom factor = scale difference
- Zoom direction = from familiar to unfamiliar

**Manim recipe (requires MovingCameraScene):**
```python
self.play(self.camera.frame.animate.set(width=4).move_to(target_pos),
          run_time=2, rate_func=smooth)
```

---

### Timeline Analogy (时间轴类比)

**Suitable for:** historical progression, evolution, technology development, lifecycle

**Visual:** Left-to-right timeline with key nodes popping up

**Variable mapping:**
- Position = time
- Node size = importance
- Color = category
- Gap = time skip

**Manim recipe:**
```python
timeline = NumberLine(x_range=[0, 10], length=12, color=T.MUTED)
milestones = [
    (2, "1903\nFlight", T.BLUE),
    (5, "1969\nMoon", T.GREEN),
    (8, "2024\nMars?", T.ORANGE),
]
for pos, label, color in milestones:
    dot = Dot(timeline.n2p(pos), color=color, radius=0.12)
    text = Text(label, font_size=16, color=color).next_to(dot, UP)
    self.play(GrowFromCenter(dot), Write(text), run_time=0.8)
```

---

### Pinball / Scattering Analogy (弹球/散射类比)

**Suitable for:** Rayleigh scattering, particle collisions, random walks, diffusion

**Visual:** Ball bouncing among obstacles vs. passing through

**Variable mapping:**
- Ball size = wavelength / particle size
- Obstacles = medium particles
- Zigzag path = scattering
- Straight path = transmission

**Manim recipe:**
```python
# See examples/sky_blue/ for a complete implementation
zigzag_path = VMobject()
zigzag_path.set_points_smoothly([np.array(p) for p in zigzag_points])
self.play(MoveAlongPath(ball, zigzag_path), run_time=4, rate_func=linear)
```

---

## Combining Patterns

Complex concepts often need 2-3 patterns in sequence:
- **Zoom → Flow**: Zoom into a cell, then show molecules flowing
- **Timeline → Chain**: Show historical progression, then the cascading consequences
- **Container → Balance**: Show resource filling up, then the trade-off of how to allocate

## Metaphor Quality Checklist

- [ ] An 8-year-old could understand the source domain (everyday object)
- [ ] The mapping has at least 3 correspondences
- [ ] The boundary is identified and addressed in narration
- [ ] The visual is self-explanatory even without narration
- [ ] No more than 1 core metaphor per 60 seconds of video

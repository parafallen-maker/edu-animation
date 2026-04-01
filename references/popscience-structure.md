# Popscience Video Structure & Density Control

## Short Video Structure (60-180 seconds)

A popscience short video has one job: **make the viewer go "哦，原来是这样！" and want to tell a friend.**

The structure is NOT a compressed lecture. It's a story with one question, one metaphor, and one aha moment.

### The 5-Beat Structure

```
Beat 1: HOOK        (5-8s)   — Grab attention with counter-intuitive fact or question
Beat 2: SETUP       (10-15s) — Establish what the viewer already knows (anchor)
Beat 3: CORE        (30-60s) — Deploy the core metaphor to explain the mechanism
Beat 4: AHA MOMENT  (5-10s)  — Connect back to the opening; the "eureka" payoff
Beat 5: LINGER      (3-5s)   — One punchy line; let it sink in; no CTA
```

### Beat Details

#### Beat 1: HOOK
- **Goal:** Create curiosity gap — viewer MUST know the answer
- **Patterns:**
  - Counter-intuitive fact: "你知道吗？你身体里的原子，大部分来自爆炸的恒星。"
  - Provocative question: "天空为什么是蓝色的？"
  - Misconception negation: "不是因为海水的倒影。"
  - Startling number: "地球上有37.2万亿个细胞。"
- **Visual:** Maximum impact, minimal elements. One bold visual + big text.
- **Density:** LOW (1-2 elements max)

#### Beat 2: SETUP
- **Goal:** Establish a familiar anchor so the metaphor has something to attach to
- **Pattern:** Start from what the viewer already knows, then reveal there's more
- **Example:** "太阳光看起来是白色的。但它其实是各种颜色混在一起。"
- **Visual:** Simple, clear, familiar imagery. No complexity yet.
- **Density:** MEDIUM (3-4 elements)

#### Beat 3: CORE METAPHOR
- **Goal:** Use the visual metaphor to explain the mechanism step by step
- **This is the soul of the video.** It should take 50-70% of total duration.
- **Pattern:** Deploy the metaphor from [metaphor-patterns.md](metaphor-patterns.md), map each element visually
- **Rules:**
  - Expand the metaphor only as far as needed — don't over-explain
  - Each sub-step: introduce ONE new element, animate it, let it breathe
  - Use a narrative pattern from [narrative-patterns.md](narrative-patterns.md) to structure the animation
- **Visual:** Progressively build complexity. This is where density peaks.
- **Density:** builds from MEDIUM to HIGH (max 6 elements), then drops

#### Beat 4: AHA MOMENT
- **Goal:** The payoff. Connect the metaphor conclusion back to the opening question.
- **Pattern:** "So [metaphor conclusion] means [real-world answer]"
- **Example:** "所以你抬头看到的蓝色，就是被弹得满天都是的蓝光。"
- **Visual:** Dramatic reduction. Strip away the metaphor scaffolding, show the answer.
- **Density:** LOW (1-2 elements). Let the conclusion breathe.

#### Beat 5: LINGER (余韵)
- **Goal:** Leave the viewer with something memorable to think about
- **Pattern:** One poetic line. NOT a summary, NOT a call-to-action.
- **Example:** "天空的颜色，是光的弹球游戏。"
- **Visual:** Minimal. Text on dark background, or a single beautiful visual.
- **Density:** LOWEST (1 element max). Silence is powerful.

---

## Density Control Rules

Visual density should breathe like a rhythm — not constant, not random.

```
Density
  HIGH │        ╱╲           
       │       ╱  ╲         
       │      ╱    ╲       
  MED  │     ╱      ╲     
       │    ╱        ╲   
       │   ╱          ╲ 
  LOW  │──╱            ╲──
       └──────────────────→ time
         hook setup core aha linger
```

### Per-Beat Density Limits

| Beat | Max Elements | Max Text Chars | Guideline |
|------|-------------|---------------|-----------|
| Hook | 2 | 8 | Full-screen single visual |
| Setup | 4 | 15 | Simple diagram |
| Core | 6 | 20 | Complex diagram, but build incrementally |
| Aha | 2 | 10 | One statement + one visual |
| Linger | 1 | 5 | Pure text or pure visual |

### Density Rules

1. **Never dump complexity.** Every element must be animated in — no "suddenly there are 10 things on screen".
2. **One new element per breath.** Animate in → let viewer absorb (0.5-1s wait) → animate next.
3. **Core section peaks, then drops.** The highest density should be at the climax of the core metaphor, followed by a deliberate strip-down into the Aha.
4. **Aha needs space.** The most important sentence must be on a near-empty screen.
5. **Linger = silence.** If the last screen still has diagrams, the viewer's mind is still processing visuals instead of feeling the message.

---

## Medium Video Structure (2-10 minutes)

For longer videos, use the 5-Beat structure as a wrapper, with the Core section expanded into multiple **chapters**, each with its own internal arc.

```
HOOK (5-10s)
SETUP (15-30s)
CORE
  ├── Chapter 1: Sub-concept A (30-90s)
  │     ├── Mini-setup
  │     ├── Mini-metaphor
  │     └── Mini-conclusion + transition
  ├── Chapter 2: Sub-concept B (30-90s)
  │     └── ...
  └── Chapter 3: Sub-concept C (30-90s)
        └── ...
AHA MOMENT (10-15s) — ties ALL chapters together
LINGER (5-10s)
```

Between chapters, use **Recap Cards** to reset cognitive load:

```python
# Recap card between chapters
recap = Z("刚才我们知道了...\n接下来看...", font_size=T.H3, color=T.BODY)
bg = RoundedRectangle(width=recap.width + 1, height=recap.height + 0.6,
                      corner_radius=0.2, fill_color=T.BG_MEDIUM, fill_opacity=0.9)
scene.play(FadeIn(VGroup(bg, recap)), run_time=0.8)
scene.wait(2)
scene.play(FadeOut(VGroup(bg, recap)), run_time=0.5)
```

---

## Educational Script Markers

Embed these markers in narration scripts (Phase 2.5) to trigger specific visual behaviors:

| Marker | Meaning | Visual Effect |
|--------|---------|---------------|
| `[THINK_PAUSE:3s]` | Question + thinking time | Show question, wait 3s silently |
| `[MISCONCEPTION]` | Common error to address | Use Misconception Correction pattern |
| `[RECAP]` | Review point | Recap card overlay |
| `[PROGRESSIVE:1/3]` | Step 1 of 3 progressive reveal | Progressive Reveal pattern |
| `[MULTI_REP:formula→graph]` | Switch representation | Show same concept in different form |
| `[DENSITY:low]` | Override density for this segment | Limit on-screen elements |

These markers are for the storyboard author. The Manim coder reads them to choose the right animation approach.

---

## Success Metrics

A popscience video succeeds if:
- [ ] A viewer can retell the core idea to a friend in one sentence
- [ ] The video works with sound off (visuals tell the story)
- [ ] Each frame has a clear focal point (not cluttered)
- [ ] The aha moment creates a felt sense of understanding, not just information
- [ ] The viewer watches to the end (linger doesn't feel like an ad)

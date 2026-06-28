# Animation Playground

Interactive demonstration of all animation components and effects.

## Quick Start

```bash
# Run the playground
python -m frontend.reflex.pages.animation_playground
```

## Components Demonstrated

### 1. Motion System

```python
from frontend.shared.design.motion import Easing, Duration

# Use predefined timings
anim_duration = Duration.fast  # 150ms
anim_easing = Easing.bounce    # Bouncy effect
```

### 2. GSAP Animations (Reflex)

```python
from frontend.reflex.components.gsap_animator import GSAPAnimator

animator = GSAPAnimator(
    targets=".element",
    x=100,
    opacity=0,
    duration=0.5,
    easing="easeInOut"
)
```

### 3. Three.js Scenes (Reflex)

```python
from frontend.reflex.components.three_scene import ThreeScene

scene = ThreeScene(
    width=800,
    height=600,
    camera_position=(0, 0, 5)
)
```

### 4. Page Transitions

```python
from frontend.reflex.components.page_transition import PageTransition

# Fade transition
transition = PageTransition(
    type="fade",
    duration=0.3
)

# Slide transition
transition = PageTransition(
    type="slide",
    direction="left",
    duration=0.4
)
```

### 5. Parallax Scrolling

```python
from frontend.reflex.components.parallax import ParallaxLayer

layers = [
    ParallaxLayer(speed=0.2, content=background),
    ParallaxLayer(speed=0.5, content=middle_ground),
    ParallaxLayer(speed=1.0, content=foreground),
]
```

### 6. Microinteractions

```python
from frontend.shared.microinteractions import Hoverable, Clickable

button = Hoverable(
    content=Button("Hover me"),
    scale=1.05,
    shadow_offset=(0, 4)
)
```

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| GSAP | ✓ | ✓ | ✓ | ✓ |
| Three.js | ✓ | ✓ | ✓ | ✓ |
| CSS Animations | ✓ | ✓ | ✓ | ✓ |
| Parallax | ✓ | ✓ | ✓ | ✓ |

## Performance Notes

- All animations use GPU-accelerated properties (transform, opacity)
- `will-change` is applied automatically to animated elements
- `prefers-reduced-motion` is respected for accessibility
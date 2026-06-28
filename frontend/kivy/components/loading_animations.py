"""Loading animations and progress indicators for Kivy.

Provides animated loading components.
"""

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.graphics import Canvas, Color, Rectangle, Ellipse
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.metrics import dp


class CircularProgress(Widget):
    """Animated circular progress indicator."""

    progress = NumericProperty(0)
    color = None
    background_color = None
    width_stroke = NumericProperty(5)
    max_value = NumericProperty(100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._angle = 0
        Clock.schedule_interval(self._update, 1/60)

    def _update(self, dt):
        """Update progress animation."""
        self._angle = (self.progress / self.max_value) * 360
        self.canvas.clear()
        with self.canvas:
            Color(*(self.background_color or [0.8, 0.8, 0.8, 1]))
            Ellipse(pos=self.pos, size=self.size, start_angle=0, angle_end=360)

            Color(*(self.color or [0.4, 0.4, 1, 1]))
            Ellipse(
                pos=self.pos,
                size=self.size,
                start_angle=self._angle - 90,
                angle_end=self._angle - 90 - (360 * (1 - self.progress / self.max_value))
            )

    def set_progress(self, value):
        """Set progress value."""
        self.progress = max(0, min(value, self.max_value))


class LoadingSpinner(Widget):
    """Spinning loading indicator."""

    spinning = BooleanProperty(True)
    color = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._angle = 0
        if self.spinning:
            Clock.schedule_interval(self._update, 1/60)

    def _update(self, dt):
        """Update rotation."""
        self._angle = (self._angle + 6) % 360
        self.rotation = self._angle

    def start(self):
        """Start spinning."""
        if not self.spinning:
            self.spinning = True
            Clock.schedule_interval(self._update, 1/60)

    def stop(self):
        """Stop spinning."""
        self.spinning = False
        Clock.unschedule(self._update)


class LoadingOverlay(Widget):
    """Full-screen loading overlay with spinner and message."""

    message = StringProperty("Carregando...")
    dismissible = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spinner = LoadingSpinner(color=[0.4, 0.4, 1, 1])
        self.spinner.size = (dp(50), dp(50))
        self.spinner.center = self.center

        self.label = Label(
            text=self.message,
            color=[1, 1, 1, 0.9],
            font_size=dp(16),
            size_hint=(None, None)
        )
        self.label.pos = (
            self.center_x - self.label.width / 2,
            self.spinner.y - dp(30)
        )

        self.add_widget(self.spinner)
        self.add_widget(self.label)

    def set_message(self, message):
        """Update overlay message."""
        self.message = message
        self.label.text = message

    def on_touch_down(self, touch):
        """Handle dismissal on touch if enabled."""
        if self.dismissible and self.collide_point(*touch.pos):
            self.parent.remove_widget(self)
            return True
        return super().on_touch_down(touch)


class ProgressBar(Widget):
    """Horizontal progress bar with animation."""

    progress = NumericProperty(0)
    bar_color = None
    background_color = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = dp(4)
        self._animating = False

    def set_progress(self, value, duration=0.3):
        """Animate progress to value."""
        if self._animating:
            return

        self._animating = True
        anim = Animation(progress=value, duration=duration)
        anim.bind(on_complete=lambda *a: setattr(self, '_animating', False))
        anim.start(self)

    def get_progress(self):
        """Get current progress value."""
        return self.progress


class IndeterminateLoader(Widget):
    """Indeterminate loading indicator (pulsing dots)."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(100), dp(40))

        # Create pulsing dots
        self.dots = []
        for i in range(3):
            dot = Widget(size_hint=(None, None), size=(dp(10), dp(10)))
            dot.x = i * dp(35)
            dot.y = 0
            dot.color = [0.4, 0.4, 1, 0.3]
            self.dots.append(dot)
            self.add_widget(dot)

        # Start animation
        Clock.schedule_interval(self._animate, 0.05)

    def _animate(self, dt):
        """Animate dots pulsing effect."""
        import math
        time = Clock.get_clock()
        for i, dot in enumerate(self.dots):
            alpha = 0.3 + 0.7 * abs(math.sin(time * 3 + i * 1))
            dot.color = [0.4, 0.4, 1, alpha]

    def stop(self):
        """Stop animation."""
        Clock.unschedule(self._animate)


__all__ = [
    'CircularProgress',
    'LoadingSpinner',
    'LoadingOverlay',
    'ProgressBar',
    'IndeterminateLoader',
]
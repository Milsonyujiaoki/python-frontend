"""Kivy ScreenManager with custom transitions.

Provides a ScreenManager with FadeTransition, SlideTransition, and other
immersive transition effects.
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty, OptionProperty
from kivy.metrics import dp

# Custom Fade Transition
class FadeTransition(NoTransition):
    """Fade in/out transition between screens."""

    duration = NumericProperty(0.3)

    def __init__(self, from_scr, to_scr, direction):
        super().__init__()
        self.from_scr = from_scr
        self.to_scr = to_scr
        self.direction = direction

    def run(self):
        """Run the fade animation."""
        self.to_scr.opacity = 0
        self.to_scr.bring_to_top()
        self.to_scr.opacity = 1
        return False


# Custom Slide Transition
class SlideTransition(NoTransition):
    """Slide in/out transition between screens."""

    duration = NumericProperty(0.3)
    sort_of = StringProperty('left')  # Direction: left, right, top, bottom

    def __init__(self, from_scr, to_scr, direction):
        super().__init__()
        self.from_scr = from_scr
        self.to_scr = to_scr
        self.direction = direction

    def run(self):
        """Run the slide animation."""
        # Get the size and position
        scr_size = self.to_scr.size
        scr_pos = list(self.to_scr.pos)

        # Calculate offset based on direction
        if self.sort_of == 'left':
            offset = scr_size[0]
        elif self.sort_of == 'right':
            offset = -scr_size[0]
        elif self.sort_of == 'top':
            offset = scr_size[1]
        else:  # bottom
            offset = -scr_size[1]

        # Set initial position based on direction
        if self.direction == 'out':
            # Screen sliding out
            if self.sort_of == 'left':
                self.from_scr.pos = [-offset, scr_pos[1]]
            elif self.sort_of == 'right':
                self.from_scr.pos = [offset + scr_pos[0], scr_pos[1]]
            elif self.sort_of == 'top':
                self.from_scr.pos = [scr_pos[0], -offset]
            else:  # bottom
                self.from_scr.pos = [scr_pos[0], offset + scr_pos[1]]
        else:  # 'in'
            # New screen sliding in
            self.to_scr.bring_to_top()

        # Animate
        anim = Animation(pos=scr_pos, duration=self.duration)
        anim.start(self.to_scr if self.direction == 'in' else self.from_scr)

        # Return the final position
        if self.direction == 'in':
            self.to_scr.pos = scr_pos
        else:
            self.from_scr.pos = scr_pos

        Clock.schedule_once(self._clear_from_scr, self.duration)
        return False

    def _clear_from_scr(self, dt):
        """Clear the from_scr position."""
        if self.from_scr and hasattr(self.from_scr, 'pos'):
            self.from_scr.pos = [0, 0]


# Custom 3D Cube Transition
class CubeTransition(NoTransition):
    """3D cube-style rotation transition between screens."""

    duration = NumericProperty(0.5)
    side = StringProperty('right')  # right, left, top, bottom

    def __init__(self, from_scr, to_scr, direction):
        super().__init__()
        self.from_scr = from_scr
        self.to_scr = to_scr
        self.direction = direction

    def run(self):
        """Run the 3D cube animation."""
        # For Kivy, we simulate 3D using 2D transforms
        self.to_scr.bring_to_top()

        # Calculate pivot based on side
        if self.side == 'right':
            pivot = (0, 0.5)
            anim_kwargs = {'rotation': 90 if self.direction == 'out' else -90}
        elif self.side == 'left':
            pivot = (1, 0.5)
            anim_kwargs = {'rotation': -90 if self.direction == 'out' else 90}
        elif self.side == 'top':
            pivot = (0.5, 1)
            anim_kwargs = {'rotation': 90 if self.direction == 'out' else -90}
        else:  # bottom
            pivot = (0.5, 0)
            anim_kwargs = {'rotation': -90 if self.direction == 'out' else 90}

        # Create animation
        anim = Animation(
            rotation=anim_kwargs.get('rotation', 0),
            duration=self.duration,
            transition='in_cubic'
        )

        # Animate the from_scr out
        if self.direction == 'out':
            anim.start(self.from_scr)
            anim.bind(on_complete=lambda *a: setattr(self.from_scr, 'rotation', 0))

        return False


# Extended ScreenManager with transition support
class EnhancedScreenManager(ScreenManager):
    """Enhanced ScreenManager with custom transition types.

    Usage:
        manager = EnhancedScreenManager(transition_type='slide', transition_duration=0.4)

    Types: 'fade', 'slide', 'cube', 'custom'
    """

    transition_type = OptionProperty('fade', options=['fade', 'slide', 'cube', 'custom'])
    transition_duration = NumericProperty(0.3)
    slide_direction = StringProperty('left')
    cube_side = StringProperty('right')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the appropriate transition
        self._set_transition()

    def _set_transition(self):
        """Set the transition based on type."""
        if self.transition_type == 'fade':
            self.transition = FadeTransition(duration=self.transition_duration)
        elif self.transition_type == 'slide':
            self.transition = SlideTransition(
                duration=self.transition_duration,
                sort_of=self.slide_direction
            )
        elif self.transition_type == 'cube':
            self.transition = CubeTransition(
                duration=self.transition_duration,
                side=self.cube_side
            )
        else:
            self.transition = NoTransition()

    def on_transition_type(self, instance, value):
        """Update transition when type changes."""
        self._set_transition()

    def on_transition_duration(self, instance, value):
        """Update transition when duration changes."""
        if hasattr(self.transition, 'duration'):
            self.transition.duration = value


# Base Screen class for consistency
class BaseScreen(Screen):
    """Base screen class with common functionality."""

    def on_enter(self):
        """Called when screen is entered."""
        pass

    def on_leave(self):
        """Called when screen is left."""
        pass

    def navigate_to(self, screen_name: str) -> None:
        """Navigate to another screen.

        Args:
            screen_name: Name of the target screen.
        """
        if self.manager:
            self.manager.current = screen_name


__all__ = [
    'FadeTransition',
    'SlideTransition',
    'CubeTransition',
    'EnhancedScreenManager',
    'BaseScreen',
]
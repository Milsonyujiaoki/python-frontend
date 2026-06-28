"""Swipe gesture handling for Kivy.

Provides swipe detection for mobile navigation.
"""

from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock
from kivy.metrics import dp


class SwipeDetector(Widget):
    """Detect and handle swipe gestures.

    Usage:
        detector = SwipeDetector(
            on_swipe_left=go_to_next_page,
            on_swipe_right=go_to_prev_page
        )
    """

    # Swipe threshold in pixels
    swipe_threshold = NumericProperty(dp(50))

    # Minimum touch distance to qualify as swipe
    min_distance = NumericProperty(dp(30))

    # Maximum time for swipe (ms)
    max_time = NumericProperty(0.5)

    # Direction triggers
    enable_left = BooleanProperty(True)
    enable_right = BooleanProperty(True)
    enable_up = BooleanProperty(True)
    enable_down = BooleanProperty(True)

    # Callbacks
    on_swipe_left = ObjectProperty(None)
    on_swipe_right = ObjectProperty(None)
    on_swipe_up = ObjectProperty(None)
    on_swipe_down = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_start_x = 0
        self._touch_start_y = 0
        self._touch_start_time = 0
        self.register_event_type('on_swipe_left')
        self.register_event_type('on_swipe_right')
        self.register_event_type('on_swipe_up')
        self.register_event_type('on_swipe_down')

    def on_touch_down(self, touch):
        """Record initial touch position."""
        if self.collide_point(*touch.pos):
            self._touch_start_x = touch.x
            self._touch_start_y = touch.y
            self._touch_start_time = Clock.get_clock()
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        """Track touch movement."""
        if touch.grab_current is self:
            # Optional: Visual feedback during swipe
            pass
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        """Detect swipe on touch release."""
        if touch.grab_current is self:
            touch.ungrab(self)

            # Calculate delta
            delta_x = touch.x - self._touch_start_x
            delta_y = touch.y - self._touch_start_y

            # Calculate time difference
            time_diff = Clock.get_clock() - self._touch_start_time

            # Check if it's a valid swipe
            if time_diff > self.max_time:
                return super().on_touch_up(touch)

            # Determine direction
            if abs(delta_x) > abs(delta_y):
                # Horizontal swipe
                if delta_x > self.min_distance and self.enable_left:
                    self.dispatch('on_swipe_left')
                elif delta_x < -self.min_distance and self.enable_right:
                    self.dispatch('on_swipe_right')
            else:
                # Vertical swipe
                if delta_y > self.min_distance and self.enable_up:
                    self.dispatch('on_swipe_up')
                elif delta_y < -self.min_distance and self.enable_down:
                    self.dispatch('on_swipe_down')

            return True
        return super().on_touch_up(touch)

    def on_swipe_left(self):
        """Called when swipe left is detected."""
        pass

    def on_swipe_right(self):
        """Called when swipe right is detected."""
        pass

    def on_swipe_up(self):
        """Called when swipe up is detected."""
        pass

    def on_swipe_down(self):
        """Called when swipe down is detected."""
        pass


class SwipeableView(Widget):
    """A view that handles swipe navigation between children.

    Usage:
        sv = SwipeableView()
        sv.add_widget(Page1())
        sv.add_widget(Page2())
        sv.add_widget(Page3())
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._current_index = 0
        self._swipe_detector = SwipeDetector(
            enable_left=True,
            enable_right=True,
            enable_up=False,
            enable_down=False,
        )
        self._swipe_detector.on_swipe_left = self._swipe_left
        self._swipe_detector.on_swipe_right = self._swipe_right

    def _swipe_left(self):
        """Navigate to next page on left swipe."""
        if self._current_index < len(self.children) - 1:
            self._current_index += 1
            self._update_pages()

    def _swipe_right(self):
        """Navigate to previous page on right swipe."""
        if self._current_index > 0:
            self._current_index -= 1
            self._update_pages()

    def _update_pages(self):
        """Update visible page with animation."""
        # Simple page swap - can be enhanced with animations
        for i, child in enumerate(self.children):
            child.opacity = 1 if i == self._current_index else 0

    def go_to_page(self, index: int):
        """Navigate to a specific page.

        Args:
            index: Page index (0-based).
        """
        if 0 <= index < len(self.children):
            self._current_index = index
            self._update_pages()

    def go_next(self):
        """Go to next page."""
        self._swipe_left()

    def go_prev(self):
        """Go to previous page."""
        self._swipe_right()

    @property
    def current_page(self):
        """Get the currently visible page."""
        if self.children and 0 <= self._current_index < len(self.children):
            return self.children[self._current_index]
        return None

    @property
    def current_index(self):
        """Get the current page index."""
        return self._current_index


class SwipeNavigation(SwipeableView):
    """Enhanced swipeable view with page indicator and smooth transitions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _update_pages(self):
        """Update pages with fade animation."""
        from kivy.animation import Animation

        for i, child in enumerate(self.children):
            if i == self._current_index:
                anim = Animation(opacity=1, duration=0.3)
                anim.start(child)
            else:
                anim = Animation(opacity=0, duration=0.3)
                anim.start(child)


__all__ = ['SwipeDetector', 'SwipeableView', 'SwipeNavigation']
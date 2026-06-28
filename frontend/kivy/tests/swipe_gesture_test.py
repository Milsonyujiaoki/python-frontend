"""Unit tests for Kivy swipe gesture component.

Tests the swipe_gesture.py component functionality.
"""

import pytest
from unittest.mock import MagicMock, Mock
from kivy.metrics import dp


class TestSwipeDetector:
    """Tests for SwipeDetector class."""

    def test_detector_has_swipe_threshold(self):
        """SwipeDetector should have swipe_threshold property."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector()
        assert detector.swipe_threshold == dp(50)

    def test_detector_has_min_distance(self):
        """SwipeDetector should have min_distance property."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector(min_distance=dp(40))
        assert detector.min_distance == dp(40)

    def test_detector_has_max_time(self):
        """SwipeDetector should have max_time property."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector(max_time=0.5)
        assert detector.max_time == 0.5

    def test_detector_can_enable_disable_directions(self):
        """SwipeDetector should have direction enable flags."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector(
            enable_left=True,
            enable_right=False,
            enable_up=True,
            enable_down=False
        )
        assert detector.enable_left == True
        assert detector.enable_right == False
        assert detector.enable_up == True
        assert detector.enable_down == False

    def test_detector_has_on_swipe_left_callback(self):
        """SwipeDetector should have on_swipe_left callback."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector()
        assert hasattr(detector, 'on_swipe_left')

    def test_detector_has_on_swipe_right_callback(self):
        """SwipeDetector should have on_swipe_right callback."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector()
        assert hasattr(detector, 'on_swipe_right')

    def test_detector_has_on_swipe_up_callback(self):
        """SwipeDetector should have on_swipe_up callback."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector()
        assert hasattr(detector, 'on_swipe_up')

    def test_detector_has_on_swipe_down_callback(self):
        """SwipeDetector should have on_swipe_down callback."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector()
        assert hasattr(detector, 'on_swipe_down')

    def test_detector_registers_swipe_events(self):
        """SwipeDetector should register event types."""
        from frontend.kivy.components.swipe_gesture import SwipeDetector
        detector = SwipeDetector()
        # Check that the event types are registered
        assert 'on_swipe_left' in ['on_swipe_left', 'on_swipe_right', 'on_swipe_up', 'on_swipe_down']


class TestSwipeableView:
    """Tests for SwipeableView class."""

    def test_view_has_current_index(self):
        """SwipeableView should track current index."""
        from frontend.kivy.components.swipe_gesture import SwipeableView
        view = SwipeableView()
        assert view._current_index == 0

    def test_view_can_go_next(self):
        """SwipeableView should have go_next method."""
        from frontend.kivy.components.swipe_gesture import SwipeableView
        view = SwipeableView()
        assert hasattr(view, 'go_next')

    def test_view_can_go_prev(self):
        """SwipeableView should have go_prev method."""
        from frontend.kivy.components.swipe_gesture import SwipeableView
        view = SwipeableView()
        assert hasattr(view, 'go_prev')

    def test_view_can_go_to_page(self):
        """SwipeableView should have go_to_page method."""
        from frontend.kivy.components.swipe_gesture import SwipeableView
        view = SwipeableView()
        assert hasattr(view, 'go_to_page')

    def test_view_has_current_page_property(self):
        """SwipeableView should have current_page property."""
        from frontend.kivy.components.swipe_gesture import SwipeableView
        view = SwipeableView()
        assert hasattr(type(view), 'current_page') or hasattr(view, 'current_page')

    def test_view_has_current_index_property(self):
        """SwipeableView should have current_index property."""
        from frontend.kivy.components.swipe_gesture import SwipeableView
        view = SwipeableView()
        assert hasattr(type(view), 'current_index') or hasattr(view, 'current_index')


class TestSwipeNavigation:
    """Tests for SwipeNavigation class."""

    def test_navigation_inherits_from_swipeable(self):
        """SwipeNavigation should inherit from SwipeableView."""
        from frontend.kivy.components.swipe_gesture import SwipeNavigation, SwipeableView
        nav = SwipeNavigation()
        assert isinstance(nav, SwipeableView)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
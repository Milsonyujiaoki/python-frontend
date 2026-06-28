"""Shared element transition for Kivy galleries.

Provides animations for element transitions between screens.
"""

from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import ObjectProperty, NumericProperty


class SharedElementTransition:
    """Manage shared element transitions between screens."""

    def __init__(self, page_container):
        self.page_container = page_container
        self.transitions = {}

    def transition_element(self, element_id, target_screen, target_pos=None):
        """Animate an element from one screen to another.

        Args:
            element_id: ID of the element to transition.
            target_screen: Target screen name.
            target_pos: Optional target (x, y) position.
        """
        if element_id not in self.transitions:
            return

        element = self.transitions[element_id]
        if not element.parent:
            return

        # Calculate current position
        current_x = element.x
        current_y = element.y

        # Get screen sizes for position calculation
        if target_pos:
            target_x, target_y = target_pos
        else:
            target_x = current_x
            target_y = current_y

        # Animate
        anim = Animation(
            x=target_x,
            y=target_y,
            duration=0.4,
            transition='out_cubic'
        )

        def on_complete(*args):
            # Move element to target screen after animation
            if target_screen in self.page_container.screen_names:
                screen = self.page_container.get_screen(target_screen)
                if screen:
                    screen.add_widget(element)

        anim.bind(on_complete=on_complete)
        anim.start(element)


class GalleryImage(Image):
    """Gallery image with shared element support."""

    element_id = ObjectProperty(None)
    is_expanded = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_stretch = True
        self.keep_ratio = True
        self.size_hint = (None, None)
        self.width = dp(150)
        self.height = dp(150)

    def on_touch_down(self, touch):
        """Handle tap to expand image."""
        if self.collide_point(*touch.pos):
            self.expand()
            return True
        return super().on_touch_down(touch)

    def expand(self):
        """Expand image to full screen."""
        anim = Animation(
            width=self.parent.width if self.parent else dp(400),
            height=self.parent.height if self.parent else dp(400),
            duration=0.3,
            transition='out_cubic'
        )
        anim.start(self)
        self.is_expanded = 1

    def collapse(self):
        """Collapse image to thumbnail size."""
        anim = Animation(
            width=dp(150),
            height=dp(150),
            duration=0.3,
            transition='out_cubic'
        )
        anim.start(self)
        self.is_expanded = 0


class SharedElementGallery(Widget):
    """Gallery with shared element transitions."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transition = SharedElementTransition(self)
        self.images = []

    def add_gallery_image(self, source, element_id=None):
        """Add an image to the gallery.

        Args:
            source: Image source path.
            element_id: Optional element ID for shared transitions.
        """
        img = GalleryImage(source=source)
        if element_id:
            img.element_id = element_id
            self.transition.transitions[element_id] = img
        self.images.append(img)
        self.add_widget(img)

    def clear_gallery(self):
        """Remove all images from gallery."""
        for img in self.images[:]:
            self.remove_widget(img)
            self.images.remove(img)


__all__ = ['SharedElementTransition', 'GalleryImage', 'SharedElementGallery']
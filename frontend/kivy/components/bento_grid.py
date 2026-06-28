"""Interactive Bento Grid component for Kivy.

Provides an animated grid layout for catalog displays.
"""

from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.properties import NumericProperty, StringProperty, ListProperty, ObjectProperty
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle


class BentoItem(Widget):
    """Single item in the bento grid with hover/tap animations."""

    title = StringProperty('')
    subtitle = StringProperty('')
    image_source = StringProperty('')
    bg_color = ListProperty([0.9, 0.9, 0.95, 1])
    icon = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_hovered = False

        with self.canvas.before:
            Color(*self.bg_color)
            self._bg = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_bg, size=self._update_bg)

        # Layout for content
        layout = GridLayout(cols=1, spacing=dp(8), padding=dp(12))
        layout.size_hint = (1, 1)
        layout.pos = self.pos
        self.add_widget(layout)

        # Title
        self.title_label = Label(
            text=self.title,
            font_size=dp(16),
            bold=True,
            halign='left',
            valign='bottom',
            size_hint_y=0.4,
        )
        layout.add_widget(self.title_label)

        # Subtitle
        self.subtitle_label = Label(
            text=self.subtitle,
            font_size=dp(12),
            opacity=0.7,
            halign='left',
            valign='bottom',
            size_hint_y=0.3,
        )
        layout.add_widget(self.subtitle_label)

        # Icon or image
        if self.image_source:
            self.image = Image(source=self.image_source, size_hint=(1, 0.3))
            layout.add_widget(self.image)
        else:
            icon_label = Label(
                text=self.icon,
                font_size=dp(32),
                halign='center',
                size_hint=(1, 0.3),
            )
            layout.add_widget(icon_label)

    def _update_bg(self, *args):
        """Update background rectangle position."""
        self._bg.pos = self.pos
        self._bg.size = self.size

    def on_title(self, instance, value):
        self.title_label.text = value

    def on_subtitle(self, instance, value):
        self.subtitle_label.text = value

    def on_image_source(self, instance, value):
        if hasattr(self, 'image'):
            self.image.source = value

    def on_touch_enter(self, touch):
        """Handle hover enter - apply lift animation."""
        if self.collide_point(*touch.pos):
            self._is_hovered = True
            anim = Animation(bg_color=[0.95, 0.95, 1, 1], duration=0.2)
            anim.start(self)
            # Add shadow effect
            self.size_hint_y = 0.32
            anim_y = Animation(y=self.y - dp(4), duration=0.2)
            anim_y.start(self)

    def on_touch_leave(self, touch):
        """Handle hover leave - restore original state."""
        if self._is_hovered:
            self._is_hovered = False
            anim = Animation(bg_color=self.bg_color, duration=0.2)
            anim.start(self)
            anim_y = Animation(y=self.y + dp(4), duration=0.2)
            anim_y.start(self)

    def on_touch_down(self, touch):
        """Handle tap - apply press animation."""
        if self.collide_point(*touch.pos):
            anim = Animation(size=(self.width * 0.98, self.height * 0.98), duration=0.1)
            anim.start(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        """Handle release - restore size."""
        anim = Animation(size=(self.width, self.height), duration=0.1)
        anim.start(self)
        return super().on_touch_up(touch)


class BentoGrid(GridLayout):
    """Bento grid layout with variable-sized cells and animations.

    Usage:
        grid = BentoGrid(
            cols=3,
            row_height=dp(120),
            spacing=dp(10),
            padding=dp(15)
        )
        grid.add_item(title="Product 1", subtitle="Description")
    """

    cols = NumericProperty(3)
    row_height = NumericProperty(120)
    spacing = NumericProperty(10)
    padding = NumericProperty(15)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = self.cols
        self.minimum_height = self.row_height + self.padding * 2

    def add_item(self, **kwargs):
        """Add a new item to the grid.

        Args:
            **kwargs: Arguments passed to BentoItem (title, subtitle, image_source, icon).
        """
        item = BentoItem(**kwargs)
        self.add_widget(item)
        return item

    def add_tall_item(self, **kwargs):
        """Add a tall item spanning 2 rows."""
        item = BentoItem(**kwargs)
        item.height = self.row_height * 2 + self.spacing
        self.add_widget(item)
        return item

    def add_wide_item(self, **kwargs):
        """Add a wide item spanning 2 columns."""
        item = BentoItem(**kwargs)
        item.width = (self.width - self.padding * 2 - self.spacing * (self.cols - 1)) / self.cols * 2
        self.add_widget(item)
        return item

    def clear_items(self):
        """Remove all items from the grid."""
        self.clear_widgets()


class BentoCatalog(BentoGrid):
    """Specialized BentoGrid for product/catalog displays.

    Pre-configured with styling for barbershop cut catalogs.
    """

    def __init__(self, **kwargs):
        super().__init__(
            cols=3,
            row_height=dp(140),
            spacing=dp(12),
            padding=dp(16),
            **kwargs
        )

    def add_cut_item(self, *, name: str, price: str, duration: str, image: str = ''):
        """Add a haircut catalog item.

        Args:
            name: Cut name.
            price: Price display (e.g., "R$ 50").
            duration: Duration (e.g., "45min").
            image: Optional image path.
        """
        self.add_item(
            title=name,
            subtitle=f"{price} • {duration}",
            image_source=image,
            icon="✂️",
            bg_color=[0.98, 0.98, 1, 1]
        )


__all__ = ['BentoItem', 'BentoGrid', 'BentoCatalog']
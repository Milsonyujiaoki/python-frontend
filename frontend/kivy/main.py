"""Kivy Hello App with ScreenManager and custom transitions."""

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

from frontend.kivy.screens.manager import EnhancedScreenManager, BaseScreen


# Build KV string for the UI
KV = """
<MainScreen>:
    orientation: 'vertical'
    padding: dp(20)
    spacing: dp(20)

    Label:
        text: "Main Screen"
        font_size: dp(40)
        halign: "center"
        valign: "middle"
        size_hint_y: 0.3

    BoxLayout:
        size_hint_y: 0.7
        spacing: dp(10)

        Button:
            text: "Go to Settings (Fade)"
            font_size: dp(20)
            on_press: root.navigate_to('settings_fade')

        Button:
            text: "Go to Profile (Slide)"
            font_size: dp(20)
            on_press: root.navigate_to('profile_slide')

        Button:
            text: "Go to Gallery (Cube)"
            font_size: dp(20)
            on_press: root.navigate_to('gallery_cube')


<SettingsScreen>:
    orientation: 'vertical'
    padding: dp(20)

    Label:
        text: "Settings Screen"
        font_size: dp(40)
        halign: "center"

    Button:
        text: "Back to Main"
        font_size: dp(20)
        on_press: root.navigate_to('main')


<ProfileScreen>:
    orientation: 'vertical'
    padding: dp(20)

    Label:
        text: "Profile Screen"
        font_size: dp(40)
        halign: "center"

    Button:
        text: "Back to Main"
        font_size: dp(20)
        on_press: root.navigate_to('main')


<GalleryScreen>:
    orientation: 'vertical'
    padding: dp(20)

    Label:
        text: "Gallery Screen"
        font_size: dp(40)
        halign: "center"

    Button:
        text: "Back to Main"
        font_size: dp(20)
        on_press: root.navigate_to('main')
"""


class MainScreen(BaseScreen):
    """Main screen with navigation buttons."""

    def on_enter(self):
        super().on_enter()
        print("Main screen entered")


class SettingsScreen(BaseScreen):
    """Settings screen."""

    def on_enter(self):
        super().on_enter()
        print("Settings screen entered")


class ProfileScreen(BaseScreen):
    """Profile screen."""

    def on_enter(self):
        super().on_enter()
        print("Profile screen entered")


class GalleryScreen(BaseScreen):
    """Gallery screen."""

    def on_enter(self):
        super().on_enter()
        print("Gallery screen entered")


class VisualDemoApp(App):
    """Kivy app demonstrating custom screen transitions."""

    def build(self):
        """Build the app with EnhancedScreenManager."""
        Builder.load_string(KV)

        # Create screens
        main_screen = MainScreen(name='main')
        settings_fade = SettingsScreen(name='settings_fade')
        profile_slide = ProfileScreen(name='profile_slide')
        gallery_cube = GalleryScreen(name='gallery_cube')

        # Create ScreenManager with different transitions
        # You can create multiple managers or change transition dynamically
        manager = EnhancedScreenManager(
            transition_type='fade',
            transition_duration=0.4,
            current='main'
        )
        manager.add_widget(main_screen)
        manager.add_widget(settings_fade)
        manager.add_widget(profile_slide)
        manager.add_widget(gallery_cube)

        return manager


if __name__ == "__main__":
    VisualDemoApp().run()
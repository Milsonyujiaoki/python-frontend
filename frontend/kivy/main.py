from kivy.app import App
from kivy.uix.label import Label


class HelloApp(App):
    def build(self):
        return Label(text="Hello, Kivy!", font_size="40sp", halign="center", valign="middle")


if __name__ == "__main__":
    HelloApp().run()
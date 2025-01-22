import kivy

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock


class Background(Widget):
    clound_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.clound_texture = Image(source="clound.png").texture
        self.clound_texture.wrap = "repeat"
        self.clound_texture.uvsize = (Window.width / self.clound_texture.width, -1)

    def scroll_texture(self, time_passed):
        self.clound_texture.uvpos = (
            (self.clound_texture.uvpos[0] + time_passed) % Window.width,
            self.clound_texture.uvpos[1],
        )
        texture = self.property("clound_texture")
        texture.dispatch(self)

    pass


class DinoRunApp(App):
    def on_start(self):
        Clock.schedule_interval(self.root.ids.background.scroll_texture, 1 / 7.5)

    pass


if __name__ == "__main__":
    DinoRunApp().run()

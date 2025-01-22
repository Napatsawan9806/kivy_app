import kivy

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock


class GameBackground(Widget):
    clound_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.clound_texture = Image(source="clound.png").texture
        self.clound_texture.wrap = "repeat"
        self.clound_texture.uvsize = (Window.width / self.clound_texture.width, -1)

        self.floor_texture = Image(source="floor.png").texture
        self.floor_texture.wrap = "repeat"
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def scroll_texture(self, time_passed):
        self.clound_texture.uvpos = (
            (self.clound_texture.uvpos[0] + time_passed / 27.0) % Window.width,
            self.clound_texture.uvpos[1],
        )

        self.floor_texture.uvpos = (
            (self.floor_texture.uvpos[0] + time_passed / 13.0) % Window.width,
            self.floor_texture.uvpos[1],
        )

        texture1 = self.property("clound_texture")
        texture2 = self.property("floor_texture")
        texture1.dispatch(self)
        texture2.dispatch(self)


class FirstPage(Screen):
    pass


class SecondPage(Screen):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.background = GameBackground()
    #     self.add_widget(self.background)
    pass


# class DinoGame(Widget):
#     background = ObjectProperty(GameBackground())

#     def update(self):
#         self.background.scroll_texture()


class DinoRunApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstPage(name="first"))
        sm.add_widget(SecondPage(name="second"))
        return sm

    def on_start(self):
        second_page = self.root.get_screen("second")
        background = second_page.ids.background
        Clock.schedule_interval(background.scroll_texture, 1 / 60.0)


if __name__ == "__main__":
    DinoRunApp().run()

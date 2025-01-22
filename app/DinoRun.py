import kivy

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock


class Background(Widget):
    clound_texture = ObjectProperty(None)
    pass


class DinoRunApp(App):
    pass


if __name__ == "__main__":
    DinoRunApp().run()

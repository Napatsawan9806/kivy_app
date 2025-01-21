import kivy

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.properties import ObjectProperty


class Background(Widget):
    pass


class DinoRunApp(App):
    def build(self):
        return Background()


if __name__ == "__main__":
    DinoRunApp().run()

import kivy

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.image import Image
from kivy.properties import ObjectProperty, NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock


class Background(Widget):
    image_one = ObjectProperty(Image)
    image_two = ObjectProperty(Image)
    image_three = ObjectProperty(Image)

    velocity_x = NumericProperty(0)
    # velocity = ReferenceListProperty(velocity_x)

    def update(self):
        self.image_one.pos = Vector(*self.velocity_x) + self.image_one.pos
        self.image_two.pos = Vector(*self.velocity_x) + self.image_two.pos
        self.image_three.pos = Vector(*self.velocity_x) + self.image_three.pos

        if self.image_one.right <= 0:
            self.image_one.pos = (self.width, 0)
        if self.image_two.right <= 0:
            self.image_two.pos = (self.width, 0)
        if self.image_three.right <= 0:
            self.image_three.pos = (self.width, 0)

    def update_position(self):
        self.image_one.pos = (0, 0)
        self.image_two.pos = (self.width, 0)
        self.image_three.pos = (self.width, 0)


class DinoRunApp(App):
    def build(self):
        return Background()


if __name__ == "__main__":
    DinoRunApp().run()

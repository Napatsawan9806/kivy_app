import kivy

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.vector import Vector
from kivy.clock import Clock


class GameBackground(Widget):
    clound_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.clound_texture = Image(source="image\clound.png").texture
        self.clound_texture.wrap = "repeat"
        self.clound_texture.uvsize = (Window.width / self.clound_texture.width, -1)

        self.floor_texture = Image(source="image\ground.png").texture
        self.floor_texture.wrap = "repeat"
        self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    def scroll_texture(self, time_passed):
        self.clound_texture.uvpos = (
            (self.clound_texture.uvpos[0] + time_passed / 27.0) % Window.width,
            self.clound_texture.uvpos[1],
        )

        self.floor_texture.uvpos = (
            (self.floor_texture.uvpos[0] + time_passed / 5.0) % Window.width,
            self.floor_texture.uvpos[1],
        )

        texture1 = self.property("clound_texture")
        texture2 = self.property("floor_texture")
        texture1.dispatch(self)
        texture2.dispatch(self)


class Dino(Widget):
    source = StringProperty("image\dino1.png")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.images = ["image\dino1.png", "image\dino2.png"]
        self.image_index = 0
        self.velocity_y = 0  # ความเร็วในแกน Y
        self.is_jumping = False  # สถานะการกระโดด
        Clock.schedule_interval(self.animate_character, 1 / 20.0)

    def animate_character(self, dt):
        self.image_index = (self.image_index + 1) % len(self.images)
        self.source = self.images[self.image_index]

    def jump(self):
        if not self.is_jumping:  # กระโดดได้เฉพาะเมื่ออยู่บนพื้น
            self.is_jumping = True
            self.velocity_y = 15  # ความเร็วเริ่มต้นของการกระโดด

    def move(self, *args):
        # การปรับความเร็วในแกน y และตำแหน่ง
        self.velocity_y -= 1  # แรงโน้มถ่วง
        self.y += self.velocity_y

        # ตรวจสอบไม่ให้ตกลงต่ำกว่าพื้น
        if self.y <= 185:
            self.y = 185
            self.velocity_y = 0
            self.is_jumping = False


class FirstPage(Screen):
    pass


class SecondPage(Screen):
    pass


class DinoRunApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstPage(name="first"))
        sm.add_widget(SecondPage(name="second"))
        return sm

    def on_start(self):

        Window.bind(on_key_down=self.on_key_down)

        second_page = self.root.get_screen("second")
        first_page = self.root.get_screen("first")
        Clock.schedule_interval(first_page.ids.background.scroll_texture, 1 / 60.0)
        Clock.schedule_interval(second_page.ids.background.scroll_texture, 1 / 60.0)

        Clock.schedule_interval(second_page.ids.dino.move, 1 / 60.0)

    def on_key_down(self, instance, key, scancode, codepoint, modifier):
        if key == 32:
            second_page = self.root.get_screen("second")
            second_page.ids.dino.jump()


if __name__ == "__main__":
    DinoRunApp().run()

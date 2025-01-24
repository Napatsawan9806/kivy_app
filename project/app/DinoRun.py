import kivy

from kivy.uix.widget import Widget
from kivy.app import App
from kivy.graphics import Rectangle
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
        self.run_image = ["image\dino1.png", "image\dino2.png"]
        self.image_index = 0
        self.jump_image = "image\dino_jump.png"
        self.velocity_y = 0  # ความเร็วในแกน Y
        self.is_jumping = False  # สถานะการกระโดด
        Clock.schedule_interval(self.animate_character, 1 / 20.0)

    def animate_character(self, dt):
        if not self.is_jumping:
            self.image_index = (self.image_index + 1) % len(self.run_image)
            self.source = self.run_image[self.image_index]

    def jump(self):
        if not self.is_jumping:  # กระโดดได้เฉพาะเมื่ออยู่บนพื้น
            self.is_jumping = True
            self.velocity_y = 23  # ความเร็วเริ่มต้นของการกระโดด

    def move(self, *args):
        # การปรับความเร็วในแกน y และตำแหน่ง
        self.velocity_y -= 1  # แรงโน้มถ่วง
        self.y += self.velocity_y
        self.source = self.jump_image

        # ตรวจสอบไม่ให้ตกลงต่ำกว่าพื้น
        if self.y <= 180:
            self.y = 180
            self.velocity_y = 0
            self.is_jumping = False
            self.source = self.run_image[self.image_index]


class Cactus(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (50, 100)
        self.x = Window.width
        self.y = 180
        self.velocity_x = 5

        with self.canvas:
            self.texture = Image(source="image/cactus.png").texture
            self.rect = Rectangle(texture=self.texture, size=(50, 50), pos=self.pos)

        # อัปเดตตำแหน่งภาพให้สอดคล้องกับ widget
        self.bind(pos=self.update_graphics_pos)

    def move(self, dt):
        self.x -= self.velocity_x
        if self.x + self.width < 0:
            self.parent.remove_widget(self)

    def update_graphics_pos(self, *args):
        # อัปเดตตำแหน่งของกราฟิก
        self.rect.pos = self.pos


class IntoGame(Screen):
    pass


class DinoGame(Screen):
    is_game_over = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.spawn_cactus, 2)
        Clock.schedule_interval(self.update, 1 / 60.0)

    def spawn_cactus(self, dt):
        if not self.is_game_over:
            cactus = Cactus()
            self.ids.game_layout.add_widget(cactus)
            print("Spawned a Cactus at", cactus.x, cactus.y)

    def update(self, dt):
        if self.is_game_over:
            return

        dino = self.ids.dino

        for child in self.ids.game_layout.children[:]:
            if isinstance(child, Cactus):
                child.move(dt)

                if dino.collide_widget(child):
                    self.game_over()

    def game_over(self):
        self.is_game_over = True
        Clock.unschedule(self.update)
        Clock.unschedule(self.spawn_cactus)
        print("Game Over!")

    def restart_game(self):
        self.is_game_over = False
        self.ids.game_layout.clear_widgets()
        self.ids.game_layout.add_widget(self.ids.dino)


class DinoRunApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(IntoGame(name="first"))
        sm.add_widget(DinoGame(name="second"))
        return sm

    def on_start(self):

        Window.bind(on_key_down=self.on_key_down)

        first_page = self.root.get_screen("first")
        second_page = self.root.get_screen("second")
        Clock.schedule_interval(first_page.ids.background.scroll_texture, 1 / 60.0)
        Clock.schedule_interval(second_page.ids.background.scroll_texture, 1 / 60.0)

        Clock.schedule_interval(second_page.ids.dino.move, 1 / 60.0)

    def on_key_down(self, instance, key, scancode, codepoint, modifier):
        if key == 32:
            second_page = self.root.get_screen("second")
            second_page.ids.dino.jump()


if __name__ == "__main__":
    DinoRunApp().run()

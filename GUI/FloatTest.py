from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


class MainWindow(Screen):
    pass


class SecondWindow(Screen):
    pass

class ThirdWindow(Screen):
    pass

class FourthWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class ImageButton(ButtonBehavior, Image):  
    pass
 
kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
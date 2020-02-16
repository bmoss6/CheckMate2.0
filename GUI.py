#Uncomment these next two lines to force Kivy to open fullscreen (what we will want when we are ready for production)
#from kivy.config import Config
#Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image 
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from game import Game
import run
import os

print("kivy")
run.main()

class MainWindow(Screen):
    pass


class PlayChessWindow(Screen):
    pass

class WatchChessWindow(Screen):
    pass

class DemoWindow(Screen):
    pass

class ShutDown(Screen):
    print ('Start Shutdown')
    os.system('pwd')
    pass

class WindowManager(ScreenManager):
    pass

class ImageButton(ButtonBehavior, Image):
    def on_press(self):  
        print ('pressed') 
    pass
 
kv = Builder.load_file("my.kv")

class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()
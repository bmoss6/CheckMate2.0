#Uncomment these next two lines to force Kivy to open fullscreen (what we will want when we are ready for production)
#from kivy.config import Config
#Config.set('graphics', 'fullscreen', 'auto')

from kivy.uix.behaviors import ButtonBehavior  
from kivy.uix.image import Image  
from kivy.lang import Builder  
from kivy.app import App  
from kivy.uix.floatlayout import FloatLayout  

class RootWidget(FloatLayout):
    pass

class ImageButton(ButtonBehavior, Image):  
    def on_press(self):  
        print ('pressed') 

class FloatChess(App):  
    def build(self):  
        return RootWidget()

if __name__ == "__main__":  
    FloatChess().run() 
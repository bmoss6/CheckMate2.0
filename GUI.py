# Uncomment these next two lines to force Kivy to open fullscreen (what we will want when we are ready for production)
# from kivy.config import Config
# Config.set('graphics', 'fullscreen', 'auto')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen


# Used to display images in demo mode:
from glob import glob
from random import randint
from os.path import join, dirname
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty

import kivy

#import run
import os
from threading import Thread

print("kivy")
#run.main()


class MainWindow(Screen):
    
    pass


class PlayChessWindow(Screen):
    pass


class WatchChessWindow(Screen):
    def on_enter(self):
        print('start game')
#        t = Thread(target=run.setup_game).start()
   
    def stop_game(self):
        print('ending game')
#        run.stop_game()
    
    def reset_game(self):
        print('resetting game')
#        run.reset_game()
        
    pass


class DemoWindow(Screen):
    pass


class PhotoWindow(Screen):
    selectedFile = 'GUIPics\Robot-Arms.png'
    def on_enter(self):  
        # the root is created in pictures.kv
        # root = self.root
        # get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'GUIPics', '*')):
            try:
                # print(filename)
                if(filename == self.selectedFile):
				    # load the image
                    picture = Picture(source=filename, size_hint=(0.98, 0.98))
                    # add to the main field	
                    self.demoPhoto = self.add_widget(picture)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)

    def on_pause(self):
        return True
    def remove_image(self):
        print('Removing the image from the PhotoWindow')
        if self.children:
            for child in self.children[:1]: # Selects the last element created (the photo)
                self.remove_widget(child)
    pass

	
class Picture(Scatter):
    '''Picture is the class that will show the image with a white border and a
    shadow. They are nothing here because almost everything is inside the
    picture.kv. Check the rule named <Picture> inside the file, and you'll see
    how the Picture() is really constructed and used.

    The source property will be the filename to show.
    '''

    source = StringProperty(None)
	

class ShutDown(Screen):
    print('Start Shutdown')
    pass


class WindowManager(ScreenManager):
    pass


class ImageButton(ButtonBehavior, Image):
    def on_press(self):
        print('pressed')

    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()

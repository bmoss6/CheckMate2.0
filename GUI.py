from kivy.config import Config
# Uncomment this next line to force kivy to open fullscreen (when ready for production)
Config.set('graphics', 'fullscreen', 'auto')

# These two lines are used to match the resolution of the touchscreen
# Config.set('graphics','width','1280')
# Config.set('graphics','height','800')

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# Modules used to display images in demo mode:
from glob import glob
from random import randint
from os.path import join, dirname
from kivy.logger import Logger
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty

import kivy
import os
from threading import Thread
import queue
import time

import run

gameStarted = False


class MainWindow(Screen):
    pass


class PlayChessWindow(Screen):
    pass


class WatchChessWindow(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.facts = "Press 'Start a Game' to begin watching a chess game!\n\nPlease be patient if ChessBot was just turned on and the button doesn't appear to be working yet.\n\nWait after pressing the button while the robots are being setup and moving into their intial position."

    #def on_enter(self):
        #self.facts = self.start_game()

    def start_game(self):
        q = queue.Queue()
        global gameStarted
        gameStarted = True;
        print('start game')
        print('start game')
        t = Thread(target=run.setup_game, args=[q]).start()
        facts = q.get()
        print(facts)
        return facts

    def stop_game(self):
        print('ending game')
        run.stop_game()
        run.lower_positions()

    def reset_game(self):
        print('resetting game')
        run.reset_game()

    pass


class DemoWindow(Screen):
	selectedFile = 'error' # If a button isn't properly selected and somehow the window goes to PhotoWindow(), load the error image
	def ChangeImage(self, filename):
		# This function will simply set the selectedFile variable to the text passsed from a selected image button
		DemoWindow.selectedFile = filename
	pass


class PhotoWindow(Screen):
	def on_enter(self):
		#curdir = dirname(__file__) # Obtain the current directory
		myFilePath = '/home/pi/Documents/CheckMate2.0/GUIPics/Diagrams/' + DemoWindow.selectedFile + '.png' # The image we want to find (selected from a button)
		print(myFilePath)
		fileFound = 0 # If the image was never found, some unknown error occurred
		for filename in glob(join('/home/pi/Documents/CheckMate2.0/GUIPics/Diagrams/', '*')): # Compare the files in GUIPics/Diagrams/
			print(filename)
			try:
				if(filename == myFilePath): # We found the image correlated with the selected button
					fileFound = 1 # Do not show the error message
					picture = Picture(source=filename) # load the image
					self.demoPhoto = self.add_widget(picture) # add to the main field	
			except Exception as e:
				Logger.exception('Pictures: Unable to load <%s>' % filename)
		if(fileFound == 0): # Some unknown error occurred finding an image
			print("Error finding photo")
			picture = Picture(source='/home/pi/Documents/GUIPics/Diagrams/error.png')
			self.demoPhoto = self.add_widget(picture)

	def on_pause(self):
		return True
	def remove_image(self):
		print('Removing the image from the PhotoWindow')
		if self.children:
			for child in self.children[:1]: # Selects the last element created (the photo)
				self.remove_widget(child) # remove it
	pass


class Picture(Scatter):
    # Picture shows the diagrams on the page, most of its format is in the kivy file
    source = StringProperty(None)


class ShutDown(Screen):
    def turn_off(self):
        if gameStarted is True:
            run.stop_game()
            run.lower_positions()
            os.system("sudo shutdown")
        if gameStarted is False:
            os.system("sudo shutdown -h now")

    def reset_pi(self):
        if gameStarted is True:
            run.stop_game()
            run.lower_positions()
        os.system("sudo shutdown -r now")

    def force_off(self):
        if gameStarted is True:
            run.stop_game()
            run.lower_positions()
        os.system("sudo shutdown -h now")
    pass


class WindowManager(ScreenManager):
    pass


class ImageButton(ButtonBehavior, Image):
    # def on_press(self):
        # print('pressed')
    pass


kv = Builder.load_file("my.kv")


class MyMainApp(App):
    facts = ""
    def build(self):
        return kv


if __name__ == "__main__":
    MyMainApp().run()

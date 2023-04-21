import logging
logger = logging.getLogger(__name__)

from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import AccountVerification
import PopUpWindow as pop
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
import PuzzleConnection
import config_file_read as parameters


class PictureScreen(Screen):
	
	def update_screen(self):
		self.update_logger()
		self.ids.imageView.source = self.parent.PUZZLE_FILE_PATH
		if self.parent.LOADED_PICTURE_TYPE=="FULL":
			self.title_picturescreen.text= parameters.get_title_full_picture() +" : "+ self.parent.LOAD_PUZZLE_NAME
		elif self.parent.LOADED_PICTURE_TYPE=="PIECES":
			self.title_picturescreen.text= parameters.get_title_pieces_picture() +" : "+ self.parent.LOAD_PUZZLE_NAME
		elif self.parent.LOADED_PICTURE_TYPE=="SOLUTION":
			self.title_picturescreen.text= parameters.get_title_solution_picture() +" : "+self.parent.LOAD_PUZZLE_NAME
			

		self.btn_goback_picture.text = parameters.get_btn_goback_picture()
		logger.info("PictureScreen: called for picture:{}".format(self.parent.PUZZLE_FILE_PATH))
		
	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)


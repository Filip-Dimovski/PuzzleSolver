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
import os
import glob
import time
import cv2
from shutil import copyfile
import config_file_read as parameters

class ChooseFileScreen(Screen):

	def update_screen(self):
		self.update_logger()
		self.btn_upload_choosefile.text = parameters.get_btn_upload_choosefile()
		self.btn_goback_choosefile.text = parameters.get_btn_goback_choosefile()
		logger.debug("ChooseFileScreen: labels are configured.")

	def open(self, path, filename):
		
		user_id = self.parent.SIGNED_USER_ID
		directory_call = self.parent.DIRECTORY_CALLED
		timestr = time.strftime("%Y%m%d_%H%M%S")
		title = parameters.get_temp_image_path()+str(user_id)+"_"+directory_call+"_"

		self.remove_older_files(title)
		
		supported_file_types = [".png", ".jpeg", ".jpg"]

		with open(os.path.join(path, filename[0])) as f:
			_, file_extension = os.path.splitext(filename[0])
	
			if file_extension not in supported_file_types:
				pop.PopupWindow.pop_up(parameters.get_notsupportedchosenfiletype_choosefile(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
				logger.warning("ChooseFileScreen: not supported file type is chosen:{}".format(file_extension))
				return

			picture_title = title+"{}.png".format(timestr)
		
			copyfile(filename[0],picture_title)

			final_picture = cv2.resize( cv2.imread( picture_title ),(600,400), interpolation = cv2.INTER_AREA) 
			cv2.imwrite(picture_title,final_picture)

			logger.info("ChooseFileScreen: file {} is copied".format(filename[0]))

		if directory_call == "FullPuzzle":
			self.parent.FULL_PUZZLE_UPLOAD=1
		if directory_call == "PiecesPuzzle":
			self.parent.PIECES_PUZZLE_UPLOAD=1

		self.parent.current = "new_puzzle"

	def selected(self, filename):
		pass
	

	def remove_older_files(self,file_name):
		for filename in glob.glob(file_name+"*.png"):
			os.remove(filename) 
			logger.info("ChooseFileScreen: file {} is removed".format(filename))
		for filename in glob.glob(file_name+"*.jpg"):
			os.remove(filename)
			logger.info("ChooseFileScreen: file {} is removed".format(filename))
		for filename in glob.glob(file_name+"*.jpeg"):
			os.remove(filename) 
			logger.info("ChooseFileScreen: file {} is removed".format(filename))

	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)



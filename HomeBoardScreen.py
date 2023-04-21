import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import AccountVerification
import os, glob,shutil
import config_file_read as parameters


class HomeBoardScreen(Screen):
	
	
	def update_screen(self):
		self.update_logger()
		if self.parent.SIGNED_USER_ID !=0:
			homeboard_label = parameters.get_title_homeboard() +", "+ AccountVerification.AccountVerification().get_user_name(self.parent.SIGNED_USER_ID)
			self.btn_mypuzzles_homeboard.disabled = False
			self.btn_manageuser_homeboard.disabled = False
			self.btn_signout_homeboard.text   = parameters.get_btn_signout_homeboard()


		if self.parent.SIGNED_USER_ID ==0:
			homeboard_label = parameters.get_title_homeboard()
			self.btn_mypuzzles_homeboard.disabled = True
			self.btn_manageuser_homeboard.disabled = True
			self.btn_signout_homeboard.text=parameters.get_btn_goback_homeboard()
			logger.debug("Homeboard:  No-user")

		self.title_homeboard.text = homeboard_label
		self.btn_manageuser_homeboard.text = parameters.get_btn_manageuser_homeboard()

		self.btn_mypuzzles_homeboard.text = parameters.get_btn_mypuzzles_homeboard()
		self.btn_newpuzzle_homeboard.text = parameters.get_btn_newpuzzle_homeboard()
		

		self.remove_old_temp_files()		
		self.parent.FULL_PUZZLE_UPLOAD = 0
		self.parent.PIECES_PUZZLE_UPLOAD = 0

		logger.debug("Homeboard: labels are configured.")


	




	def sign_out(self):
		self.parent.SIGNED_USER_ID = 0
		self.parent.current = "main"
		logger.info("Homeboard: User has signed out")

	def remove_old_temp_files(self):
		user_id = self.parent.SIGNED_USER_ID
		title = parameters.get_temp_image_path()+str(user_id)
		for filename in glob.glob(title+"*.png"):
			os.remove(filename) 
			logger.info("Homeboard: file {} is removed.".format(filename))

	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

	
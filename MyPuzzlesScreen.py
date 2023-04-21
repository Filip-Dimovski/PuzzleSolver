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
import AccountVerification



class MyPuzzlesScreen(Screen):

	def update_screen(self):
		self.update_logger()
		self.title_mypuzzles.text = parameters.get_title_mypuzzles()+' (' + str(AccountVerification.AccountVerification().count_user_puzzle(self.parent.SIGNED_USER_ID)) + ')'
		self.btn_goback_mypuzzles.text = parameters.get_btn_goback_mypuzzles()
		self.fill_data()
		logger.debug("MyPuzzleScreen: puzzles are loaded")
	
	def fill_data(self):
		user_id = self.parent.SIGNED_USER_ID
		puzzles = self.get_puzzles(user_id)
		self.rv.data = [{'value': '' + puzzle} for puzzle in puzzles]

		

	def get_puzzles(self,user_id):
		
		return PuzzleConnection.PuzzleConnection().fetch_all_puzzles(user_id)


	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)


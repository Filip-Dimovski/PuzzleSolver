
from kivy.app import App
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager
import PuzzleConnection
import logging
import time
import config_file_read as parameters


class RootScreen(ScreenManager):
	LOG_PATH=""
	LOG_LEVEL=""
	LOG_FORMATTER = parameters.get_logging_formatter()
	USED_LANGUAGE = ""
	SIGNED_USER_ID = 0
	CAMERA_CALLED = ""
	DIRECTORY_CALLED = ""
	FULL_PUZZLE_UPLOAD = 0
	PIECES_PUZZLE_UPLOAD = 0
	LOAD_PUZZLE_NAME = ""
	LOAD_PUZZLE_ID = 0
	PUZZLE_FILE_PATH=""
	NOUSER_PUZZLE_FILE_PATH =""
	LOADED_PICTURE_TYPE=""

	log_level_dict = {
	"DEBUG": logging.DEBUG,
	"INFO": logging.INFO,
	"WARNING": logging.WARNING,
	"ERROR": logging.ERROR,
	"CRITICAL": logging.CRITICAL
	}

	timestr = time.strftime("%Y%m%d")
	logger = logging.getLogger(__name__)
	LOG_LEVEL = log_level_dict[parameters.get_logging_level().upper()]
	logger.setLevel(LOG_LEVEL)
	formatter = logging.Formatter(LOG_FORMATTER)
	LOG_PATH = parameters.get_logging_path()+'{}.log'.format(timestr)

	file_handler = logging.FileHandler(LOG_PATH)
	file_handler.setFormatter(formatter)
	logger.addHandler(file_handler)
	logger.info('RootScreen: App has started')



	def update_puzzle_name(self,selected_puzzle):
		self.LOAD_PUZZLE_NAME = selected_puzzle
		self.LOAD_PUZZLE_ID = PuzzleConnection.PuzzleConnection().get_puzzle_id(selected_puzzle,self.SIGNED_USER_ID)
		self.current = "picture_view"

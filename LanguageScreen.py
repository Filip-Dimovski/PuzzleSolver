import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import  Screen
from configparser import ConfigParser
import config_file_read as parameters


class LanguageScreen(Screen):
	

	
	def update_language_eng(self):
		self.parent.USED_LANGUAGE = "en"
		self.update_logger()
		logger = logging.getLogger(__name__)
		logger.debug("LanguageScreen: en language is used")


	def update_language_mkd(self):
		self.parent.USED_LANGUAGE = "mk"
		self.update_logger()
		logger.debug("LanguageScreen: mk language is used")


	def update_logger(self):
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

		


	# def update_config_file(self,value):
	# 	config = ConfigParser()
	# 	config.read('config/config.ini')
	# 	cfgfile = open('config/config.ini','w')
	# 	config.set('settings', 'default_language', str(value))
	# 	config.write(cfgfile)
	# 	cfgfile.close()
		

    


		

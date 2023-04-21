import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import AccountVerification
import PopUpWindow as pop
from kivy.lang import Builder
import PuzzleConnection
import config_file_read as parameters
import os,glob
import shutil
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class PictureViewScreen(Screen):
	def update_screen(self):
		self.update_logger()
		puzzle_name = self.parent.LOAD_PUZZLE_NAME
		self.title_pictureview.text =parameters.get_title_pictureview() + puzzle_name
		self.btn_fullpuzzle_pictureview.text = parameters.get_btn_fullpuzzle_pictureview()
		self.btn_piecespuzzle_pictureview.text = parameters.get_btn_piecespuzzle_pictureview()
		self.btn_deletepuzzle_pictureview.text = parameters.get_btn_deletepuzzle_pictureview()
		self.btn_solution_pictureview.text = parameters.get_btn_solution_pictureview()
		self.btn_goback_pictureview.text = parameters.get_btn_goback_pictureview()
		
		if self.parent.SIGNED_USER_ID == 0:
			self.btn_deletepuzzle_pictureview.disabled = True
		elif self.parent.SIGNED_USER_ID != 0:
			self.btn_deletepuzzle_pictureview.disabled = False

		logger.debug("PictureViewScreen: labels are configured")

		

	def full_puzzle_on_click(self):
		if self.parent.SIGNED_USER_ID !=0:
			puzzle_id = self.parent.LOAD_PUZZLE_ID
			puzzle_path = PuzzleConnection.PuzzleConnection().get_puzzle_full_path(puzzle_id) 
			self.parent.PUZZLE_FILE_PATH = puzzle_path
			
		else:
			self.parent.PUZZLE_FILE_PATH = self.parent.NOUSER_PUZZLE_FILE_PATH + '/FullPuzzle.png'

		self.parent.LOADED_PICTURE_TYPE="FULL"
		logger.debug("PictureViewScreen: full_puzzle_on_click is called for puzzle: {} ".format(self.parent.PUZZLE_FILE_PATH))
		self.parent.current = "picture"


	def pieces_puzzle_on_click(self):
		if self.parent.SIGNED_USER_ID != 0:
			puzzle_id = self.parent.LOAD_PUZZLE_ID
			puzzle_path = PuzzleConnection.PuzzleConnection().get_puzzle_pieces_path(puzzle_id) 
			self.parent.PUZZLE_FILE_PATH = puzzle_path
						
		else:
			self.parent.PUZZLE_FILE_PATH = self.parent.NOUSER_PUZZLE_FILE_PATH +'/PiecesPuzzle.png'

		self.parent.LOADED_PICTURE_TYPE="PIECES"
		logger.debug("PictureViewScreen: pieces_puzzle_on_click is called for puzzle: {} ".format(self.parent.PUZZLE_FILE_PATH))
		self.parent.current = "picture"

	def btn_deletepuzzle_on_click(self):
		popup_title = parameters.get_deletepuzzle_title()+ self.parent.LOAD_PUZZLE_NAME
		popup_label = parameters.get_deletepuzzle_label()
		popup_yesbutton = parameters.get_deletepuzzle_yesbutton()
		popup_nobutton = parameters.get_deletepuzzle_nobutton()
		layout      = GridLayout(cols=1, padding=40)
		popupLabel  = Label(text  = popup_label,font_size=20,color=[0,0,0,1],halign = 'center')
		yes_button = Button(text = popup_yesbutton ,size= (75, 50))
		no_button = Button(text = popup_nobutton,size= (75, 50))
		layout.add_widget(popupLabel)
		layout.add_widget(yes_button)
		layout.add_widget(no_button)       
		popup = Popup(title=popup_title,content=layout, background = parameters.get_popup_background(),size_hint=(None, None), size=(400, 400),title_color=[0,0,0,1],title_size='20sp',title_align='center') 
		popup.open()   
		logger.debug("PictureViewScreen: delete puzzle popup")
		no_button.bind(on_press=popup.dismiss)   
		yes_button.bind(on_press=self.delete_puzzle)
		yes_button.bind(on_press=popup.dismiss)


	def delete_puzzle(self,instance):
		logger.info("PictureViewScreen: delete puzzle is called")
		puzzle_path = PuzzleConnection.PuzzleConnection().get_puzzle_folder_path(self.parent.LOAD_PUZZLE_ID) 
		PuzzleConnection.PuzzleConnection().delete_puzzle(self.parent.LOAD_PUZZLE_ID)
		self.remove_puzzle_data(puzzle_path)
		self.parent.LOAD_PUZZLE_ID = 0
		self.parent.current = "my_puzzles"


	def remove_puzzle_data(self,puzzle_path):
		
		for the_file in os.listdir(puzzle_path):
			file_path = os.path.join(puzzle_path, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
					logger.info("PictureViewScreen: file {} is removed.".format(file_path))
				elif os.path.isdir(file_path): 
					shutil.rmtree(file_path)
					logger.info("PictureViewScreen: Directory {} is removed.".format(file_path))
			except Exception as e:
				logger.exception(e)

		shutil.rmtree(puzzle_path)



	def solution_puzzle_on_click(self):

		if self.parent.SIGNED_USER_ID != 0:
			puzzle_id = self.parent.LOAD_PUZZLE_ID
			puzzle_path = PuzzleConnection.PuzzleConnection().get_puzzle_solution_path(puzzle_id) 
			self.parent.PUZZLE_FILE_PATH = puzzle_path

			
		else:
			self.parent.PUZZLE_FILE_PATH = self.parent.NOUSER_PUZZLE_FILE_PATH +'/SolutionPuzzle.png'

		self.parent.LOADED_PICTURE_TYPE="SOLUTION"
		logger.debug("PictureViewScreen: solution_puzzle_on_click is called for puzzle: {} ".format(self.parent.PUZZLE_FILE_PATH))
		self.parent.current = "picture"


	def btn_goback_on_click(self):

		logger.debug("PictureViewScreen: btn_goback is clicked")
		if self.parent.SIGNED_USER_ID !=0:
			self.parent.current = "my_puzzles"
		else:
			self.remove_no_user_puzzle()
			self.parent.current='homeboard'

	def remove_no_user_puzzle(self):
		folder_name = self.parent.NOUSER_PUZZLE_FILE_PATH

		for the_file in os.listdir(folder_name):
			file_path = os.path.join(folder_name, the_file)
			try:
				if os.path.isfile(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path): shutil.rmtree(file_path)
				logger.info("PictureViewScreen: File:{} is removed".format(file_path))
			except Exception as e:
				print(e)
		shutil.rmtree(folder_name)
		logger.info("PictureViewScreen: Folder: {} is removed. ".format(folder_name))
		self.parent.NOUSER_PUZZLE_FILE_PATH=""

	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

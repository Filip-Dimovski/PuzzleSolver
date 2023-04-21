import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
import PopUpWindow as pop
import os, glob
from kivy.lang import Builder
from pathlib import Path
import time
import PuzzleConnection
import config_file_read as parameters
import PuzzleSolution as solution
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar


class NewPuzzleScreen(Screen):

	def update_screen(self):
		self.update_logger()
		self.title_newpuzzle.text = parameters.get_title_newpuzzle()
		self.label_puzzlename_newpuzzle.text = parameters.get_label_puzzlename_newpuzzle()
		self.label_fullpicture_newpuzzle.text = parameters.get_label_fullpicture_newpuzzle()
		self.btn_fullpuzzlecamera_newpuzzle.text = parameters.get_label_fullpicturecamera_newpuzzle()
		self.btn_fullpuzzledirectory_newpuzzle.text = parameters.get_label_fullpicturedirectory_newpuzzle()
		self.label_piecespuzzle_newpuzzle.text = parameters.get_label_piecespuzzle_newpuzzle()
		self.btn_piecespuzzlecamera_newpuzzle.text = parameters.get_label_piecespicturecamera_newpuzzle()
		self.btn_piecespuzzledirectory_newpuzzle.text = parameters.get_label_piecespicturedirectory_newpuzzle()
		self.btn_solvepuzzle_newpuzzle.text = parameters.get_btn_solvepuzzle_newpuzzle()
		self.btn_goback_newpuzzle.text = parameters.get_btn_goback_newpuzzle()
		if self.parent.FULL_PUZZLE_UPLOAD == 0:
			self.img_fullpicture_newpuzzle.source = parameters.get_x_image_path()
		else:
			self.img_fullpicture_newpuzzle.source = parameters.get_tick_image_path()
		if self.parent.PIECES_PUZZLE_UPLOAD ==0:
			self.img_piecespicture_newpuzzle.source = parameters.get_x_image_path()
		else:
			self.img_piecespicture_newpuzzle.source = parameters.get_tick_image_path()


		logger.debug("NewPuzzleScreen: labels are configured")


	def go_back(self):
		self.remove_old_temp_files()
		self.parent.FULL_PUZZLE_UPLOAD=0
		self.parent.PIECES_PUZZLE_UPLOAD=0
		self.new_puzzle_name.text =""
		logger.debug("NewPuzzleScreen: go_back is called.")

	def remove_old_temp_files(self):
		user_id = self.parent.SIGNED_USER_ID
		title = parameters.get_temp_image_path()+str(user_id)
		for filename in glob.glob(title+"*.png"):
			os.remove(filename) 
			logger.info("NewPuzzleScreen: File:{} is removed.".format(filename))


	def update_camera_call(self,call_camera):
		self.parent.CAMERA_CALLED = call_camera
		logger.debug("NewPuzzleScreen: CAMERA_CALLED is changed to {}".format(call_camera))

	def btn_solve_puzzle_on_press(self):
		if self.check_inputs():
			self.create_puzzle_user()
			self.parent.LOAD_PUZZLE_NAME = self.new_puzzle_name.text
			if self.parent.SIGNED_USER_ID !=0:
				folder_path = PuzzleConnection.PuzzleConnection().get_puzzle_folder_path(self.parent.LOAD_PUZZLE_ID)
			else:
				folder_path = self.parent.NOUSER_PUZZLE_FILE_PATH

			puzzle_solution = solution. PuzzleSolution(folder_path)
			puzzle_solution.solve_puzzle()
			solution_path = folder_path+"//SolutionPuzzle.png"
			PuzzleConnection.PuzzleConnection().update_puzzle_solution(self.parent.LOAD_PUZZLE_ID,solution_path)
			logger.info("NewPuzzleScreen: Puzzle is solved.")
			self.new_puzzle_name.text =""
			self.parent.current = "picture_view"



	def update_directory_call(self,call_directory):
		self.parent.DIRECTORY_CALLED = call_directory
		logger.debug("NewPuzzleScreen: DIRECTORY_CALLED is changed to {}".format(call_directory))
			




	def create_puzzle_user(self):
		puzzle_name=self.new_puzzle_name.text
		user_id = self.parent.SIGNED_USER_ID
		timestr = time.strftime("%Y%m%d_%H%M%S")
		folder_name = parameters.get_user_path()+str(user_id)+"/"+puzzle_name+"_{}".format(timestr) 	
		os.mkdir(folder_name)

		logger.info("NewPuzzleScreen: Folder {} is created.".format(folder_name))
		
		if self.parent.SIGNED_USER_ID ==0:
			self.parent.NOUSER_PUZZLE_FILE_PATH = folder_name

		file_names = parameters.get_temp_image_path()+str(user_id)+"*.png"
		for filename in glob.glob(file_names):
			if "FullPuzzle" in filename:
				os.rename(filename, folder_name+"/FullPuzzle.png")
				logger.info("NewPuzzleScreen: file {} is moved".format(folder_name+"/FullPuzzle.png"))
			if "PiecesPuzzle" in filename:
				os.rename(filename, folder_name+"/PiecesPuzzle.png")
				logger.info("NewPuzzleScreen: file {} is moved".format(folder_name+"/PiecesPuzzle.png"))
		if user_id != 0:
			PuzzleConnection.PuzzleConnection().create_puzzle(puzzle_name,folder_name,user_id)
			PuzzleConnection.PuzzleConnection().create_puzzle_user_rel(puzzle_name,user_id)
			self.parent.LOAD_PUZZLE_ID = PuzzleConnection.PuzzleConnection().get_puzzle_id(self.new_puzzle_name.text,self.parent.SIGNED_USER_ID)
			

	def check_inputs(self):
		puzzle_name=self.new_puzzle_name.text
		user_id = self.parent.SIGNED_USER_ID
		if not puzzle_name:
			pop.PopupWindow.pop_up(parameters.get_noname_puzzle_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.warning("NewPuzzleScreen: {} ".format(parameters.get_noname_puzzle_popup_warnings()))
			return False
		if (PuzzleConnection.PuzzleConnection().check_user_puzzle_rel(puzzle_name,user_id)) == True:
			pop.PopupWindow.pop_up(parameters.get_name_exists_puzzle_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.warning("NewPuzzleScreen: {}".format(parameters.get_name_exists_puzzle_popup_warnings()))
			return False
		if self.parent.FULL_PUZZLE_UPLOAD == 0:
			pop.PopupWindow.pop_up(parameters.get_no_full_puzzle_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.warning("NewPuzzleScreen: {}".format(parameters.get_no_full_puzzle_popup_warnings()))
			return False
		if self.parent.PIECES_PUZZLE_UPLOAD == 0:
			pop.PopupWindow.pop_up(parameters.get_no_pieces_puzzle_popup_warnings(),parameters.get_title_popup_warnings(),parameters.get_popup_button_popup_warnings())
			logger.warning("NewPuzzleScreen: {}".format(parameters.get_no_pieces_puzzle_popup_warnings()))
			return False
		return True

	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)

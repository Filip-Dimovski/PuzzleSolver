import logging
logger = logging.getLogger(__name__)
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
import time
from kivy.base import EventLoop
import os, glob
import cv2
import config_file_read as parameters

class CameraScreen(Screen):

	def update_screen(self):
		self.update_logger()
		self.label_goback_camera.text = parameters.get_label_goback_camera()
		self.btn_capture_camera.text = parameters.get_btn_capture_camera()
		logger.debug("CameraScreen: labels configured.")

	def go_back(self):
		self.parent.current = "new_puzzle"
		logger.debug("CameraScreen: go_back is called.")

	def capture(self):
		camera = self.ids['camera']
		timestr = time.strftime("%Y%m%d_%H%M%S")
		user_id = self.parent.SIGNED_USER_ID
		camera_call = self.parent.CAMERA_CALLED
		title = parameters.get_temp_image_path()+str(user_id)+"_"+camera_call+"_"
		
		self.remove_older_files(title)
		
		picture_title = title+"{}.png".format(timestr)
		camera.export_to_png(picture_title)

		final_picture = cv2.resize(cv2.imread(picture_title),(600,400), interpolation = cv2.INTER_AREA) 
		cv2.imwrite(picture_title,final_picture)

		logger.info("CameraScreen: image {} is created.".format(picture_title))

		if camera_call == "FullPuzzle":
			self.parent.FULL_PUZZLE_UPLOAD=1
		if camera_call == "PiecesPuzzle":
			self.parent.PIECES_PUZZLE_UPLOAD=1
		
		self.parent.current = "new_puzzle"



	def remove_older_files(self,file_name):
		for filename in glob.glob(file_name+"*.png"):
			os.remove(filename) 
			logger.info("CameraScreen: file {} is removed".format(filename))
		for filename in glob.glob(file_name+"*.jpg"):
			os.remove(filename)
			logger.info("CameraScreen: file {} is removed".format(filename))
		for filename in glob.glob(file_name+"*.jpeg"):
			os.remove(filename)
			logger.info("CameraScreen: file {} is removed".format(filename))

	def update_logger(self):
		if logger.handlers:
			return
		logger.setLevel(self.parent.LOG_LEVEL)
		formatter = logging.Formatter(self.parent.LOG_FORMATTER)
		file_handler = logging.FileHandler(self.parent.LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)
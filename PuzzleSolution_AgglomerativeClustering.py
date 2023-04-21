import logging
logger = logging.getLogger(__name__)
import cv2
import numpy as np
from matplotlib import pyplot as plt
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
import config_file_read as parameters
import _thread
import threading
import time
import pandas as pd
from sklearn.datasets.samples_generator import make_blobs
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from collections import Counter, defaultdict
from statistics import mean 
from scipy.cluster.hierarchy import ward, fcluster
from scipy.spatial.distance import pdist
import math
from operator import itemgetter 

class PuzzleSolution(Widget):
	progress_bar = ObjectProperty()
	stop = threading.Event()

	def __init__(self, folder_path_io,**kwa):
		self.folder_path = folder_path_io
		self.update_logger()
		self.update_progress  = False
		self.progress_bar_value = 3
		super(PuzzleSolution, self).__init__(**kwa)
		self.progress_bar = ProgressBar()
		self.popup = Popup(title=parameters.get_progress_bar_title(),content=self.progress_bar, background = parameters.get_popup_background(),size_hint=(None, None), size=(400, 400),title_color=[0,0,0,1],title_size='20sp',title_align='center')
		self.popup.bind(on_open=self.puopen)
		self.pop(self)
		logger.debug("PuzzleSolution: initialize")

	def pop(self, instance):
		self.progress_bar.value = 1
		self.popup.open()
		logger.debug("PuzzleSolution: progressbar pop is open")

	def next(self, dt):
		if self.progress_bar.value>=100:
			return False
			logger.info("PuzzleSolution: progress_bar has stopped.")
		self.progress_bar.value+=self.progress_bar_value
		
		logger.debug("PuzzleSolution: progress_bar.value ={}".format(self.progress_bar.value))
        

	def puopen(self, instance):
		Clock.schedule_interval(self.next, 1)


	def solve_puzzle(self):
		logger.debug("PuzzleSolution: solve_puzzle is called.")
		threading.Thread(target=self.solve_puzzle_algorithm).start()


	def solve_puzzle_algorithm(self):

		logger.debug("PuzzleSolution: solve_puzzle_algorithm is called.")
		full_puzzle_name = self.folder_path+'/FullPuzzle.png'
		pieces_puzzle_name = self.folder_path+'/PiecesPuzzle.png'
		pieces_puzzle = cv2.resize(cv2.imread(pieces_puzzle_name),(600,400), interpolation = cv2.INTER_AREA) 

		full_puzzle = cv2.resize(cv2.imread(full_puzzle_name),(600,400), interpolation = cv2.INTER_AREA) 

		cv2.imwrite(full_puzzle_name,full_puzzle)
		cv2.imwrite(pieces_puzzle_name,pieces_puzzle)

		copy_pieces_puzzle = pieces_puzzle.copy()

		pieces_puzzle_gray = cv2.cvtColor(pieces_puzzle, cv2.COLOR_BGR2GRAY) 
		full_puzzle_gray = cv2.cvtColor(full_puzzle,cv2.COLOR_BGR2GRAY)

		retval, pieces_puzzle_gray =cv2.threshold(pieces_puzzle_gray,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		kernel = np.ones((5,5), np.uint8)
		pieces_puzzle_gray_erosion = cv2.erode(pieces_puzzle_gray, kernel, iterations = 2) 

		pieces_puzzle_gray_edges = cv2.Canny(pieces_puzzle_gray_erosion, 100, 200) 

		#cv2.imshow("",pieces_puzzle_gray_edges)

		
		_,contours, hierarchy = cv2.findContours(pieces_puzzle_gray_edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
		logger.info("PuzzleSolution: Number of Contours found = {}".format(str(len(contours))))

		solution_name = self.folder_path+'/SolutionPuzzle.png'

		if len(contours) ==0:
			self.popup.dismiss()
			self.progress_bar_value = 100
		else:
			self.progress_bar_value = 100/len(contours)

		Clock.schedule_once(self.puopen, 0)
		#print("LEN CONTOUR: "+ str(len(contours)) )
		#print("PROGRESS VALUEEE: " + str(self.progress_bar_value)) 

		cv2.imwrite(solution_name,full_puzzle.copy())

		number_contours = len(contours)

		contours_height=[]
		contours_width=[]
		
		for contours_part in contours:
			rect = cv2.boundingRect(contours_part)
			_,_,w,h = rect
			if h>10:#(400/number_contours)/10:
				contours_height.append(h)
			if w>10:#(600/number_contours)/10:
				contours_width.append(w)

		contours_height=sorted(contours_height)
		contours_width=sorted(contours_width)

		contours_height_q1, contours_height_q3= np.percentile(contours_height,[25,75])
		contours_height_iqr = contours_height_q3 - contours_height_q1
		contours_height_lower_bound = contours_height_q1 -(1.5 * contours_height_iqr) 
		contours_height_upper_bound = contours_height_q3 +(1.5 * contours_height_iqr) 


		contours_width_q1, contours_width_q3= np.percentile(contours_width,[25,75])
		contours_width_iqr = contours_width_q3 - contours_width_q1
		contours_width_lower_bound = contours_width_q1 -(1.5 * contours_width_iqr) 
		contours_width_upper_bound = contours_width_q3 +(1.5 * contours_width_iqr) 

		height_elements = np.array(contours_height)
		height_mean = np.mean(height_elements, axis=0)
		height_sd = np.std(height_elements, axis=0)
		height_final_list = [x for x in contours_height if (x > height_mean - 2 * height_sd)]
		height_final_list = [x for x in height_final_list if (x < height_mean + 2 * height_sd)]


		width_elements = np.array(contours_width)
		width_mean = np.mean(width_elements, axis=0)
		width_sd = np.std(width_elements, axis=0)
		width_final_list = [x for x in contours_width if (x > width_mean - 2 * width_sd)]
		width_final_list = [x for x in width_final_list if (x < width_mean + 2 * width_sd)]

		#print("HM: "+str(height_mean) + " HSD: "+str(height_sd))
		#print("WM: "+str(width_mean) + " WSD: "+str(width_sd))

		# print(width_final_list)
		# print(height_final_list)
		contour_cnt = 0
		for contours_part in contours:
						
			countour_list = contours_part.tolist()
			rect = cv2.boundingRect(contours_part)
			x,y,w,h = rect
			#print("W: "+str(w)+ " H: "+str(h))
			if w<contours_width_lower_bound or h<contours_height_lower_bound:
			#if w not in width_final_list or h not in height_final_list: 
				continue

			if w>contours_width_upper_bound or h>contours_height_upper_bound:
				continue

			contour_cnt+=1
			box = cv2.rectangle(copy_pieces_puzzle, (x,y), (x+w,y+h), (0,0,255), 2)
			cropped = copy_pieces_puzzle[y: y+h, x: x+w]
			part_name = self.folder_path+"/piece"+str(contour_cnt)+".png"
			cv2.imwrite(part_name, cropped)
			logger.debug("PuzzleSolution:  part puzzle {} is created".format(part_name))
			max_distance = math.sqrt( w*w + h*h)
			res_feature_matches = self.feature_matches(part_name,full_puzzle_name,solution_name,contour_cnt,max_distance)
			if res_feature_matches:
				cv2.drawContours(pieces_puzzle, contours_part, -1, (0, 255,0), 2) 
				cv2.putText(pieces_puzzle, str(contour_cnt), tuple(tuple(countour_list[0])[0]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), lineType=cv2.LINE_AA)
			else:
				cv2.drawContours(pieces_puzzle, contours_part, -1, (0, 0, 255), 2) 
				cv2.putText(pieces_puzzle, str(contour_cnt), tuple(tuple(countour_list[0])[0]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), lineType=cv2.LINE_AA)
			

		solution_puzzle = cv2.imread(solution_name,1)
		result = np.concatenate((solution_puzzle, pieces_puzzle), axis=1)
		cv2.imwrite(solution_name,result)
		self.popup.dismiss()
		return solution_name

	def feature_matches(self,part_puzzle_name,full_puzzle_name,solution_name,part_number,max_distance):
		try:
			logger.debug("PuzzleSolution:  future_matches is called.")
			full_puzzle = cv2.imread(full_puzzle_name,0)
			part_puzzle = cv2.imread(part_puzzle_name,0)
			solution_puzzle = cv2.imread(solution_name,1)

			sift = cv2.xfeatures2d.SIFT_create()

			# find the keypoints and descriptors with SIFT
			kp1, des1 = sift.detectAndCompute(full_puzzle,None)
			kp2, des2 = sift.detectAndCompute(part_puzzle,None)

			bf = cv2.BFMatcher()
			matches = bf.knnMatch(des1,des2, k=2)

			good = []
			list_points = []
			for m,n in matches:
				if m.distance < 0.55*n.distance:
					img1_idx = m.queryIdx
					x,y = kp1[img1_idx].pt 
					list_points.append((x,y))
					good.append([m])
			
			if not good:
				logger.debug("PuzzleSolution:  future_matches not match found")
				return False


			Z = ward(pdist(list_points))
			array = fcluster(Z, t=max_distance, criterion='distance')
			
			counts = np.bincount(array)
			leading_cluster = np.argmax(counts)
			
			leading_cluster_points_idx = np.where(array == leading_cluster)
			leading_cluster_points_idx = (leading_cluster_points_idx[0]).tolist()

			points = itemgetter(*leading_cluster_points_idx)(list_points)
			avg_point_x = mean(value[0] for value in points)
			avg_point_y = mean(value[1] for value in points)


			cv2.putText(solution_puzzle, str(part_number), (int(avg_point_x) , int(avg_point_y) ) , cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), lineType=cv2.LINE_AA) 
			logger.debug("PuzzleSolution:  future_matches match found at: {}".format(str(avg_point_x)+ " : "+str(avg_point_y)) )
			cv2.imwrite(solution_name,solution_puzzle)
		
			return True
			
		except:
			return False

	def update_logger(self):
		
		log_level_dict = {
		"DEBUG": logging.DEBUG,
		"INFO": logging.INFO,
		"WARNING": logging.WARNING,
		"ERROR": logging.ERROR,
		"CRITICAL": logging.CRITICAL
		}

		timestr = time.strftime("%Y%m%d")
		logger = logging.getLogger(__name__)
		if logger.handlers:
			return
		log_level = log_level_dict[parameters.get_logging_level().upper()]
		logger.setLevel(log_level)
		formatter = logging.Formatter(parameters.get_logging_formatter())
		LOG_PATH = parameters.get_logging_path()+'{}.log'.format(timestr)
		file_handler = logging.FileHandler(LOG_PATH)
		file_handler.setFormatter(formatter)
		logger.addHandler(file_handler)



# folder_path_io='C:\\Users\\Filip.Dimovski\\Documents\\PuzzleSolver\\users\\0\\ttt_20191110_170143'
# pt = PuzzleSolution(folder_path_io)
# pt.solve_puzzle()

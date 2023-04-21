import cv2
import numpy as np
from matplotlib import pyplot as plt
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

class PuzzleSolution():

	def __init__(self, folder_path_io,**kwa):
		self.folder_path = folder_path_io


	def solve_puzzle_algorithm(self):

		full_puzzle_name = self.folder_path+'/FullPuzzle.png'
		pieces_puzzle_name = self.folder_path+'/PiecesPuzzle.png'
		
		
		final_picture_1 = cv2.resize(cv2.imread(full_puzzle_name),(600,400), interpolation = cv2.INTER_AREA) 
		final_picture_2 = cv2.resize(cv2.imread(pieces_puzzle_name),(600,400), interpolation = cv2.INTER_AREA) 
		cv2.imwrite(full_puzzle_name,final_picture_1)
		cv2.imwrite(pieces_puzzle_name,final_picture_2)


		pieces_puzzle = cv2.imread(pieces_puzzle_name)
		full_puzzle = cv2.imread(full_puzzle_name) 


		copy_pieces_puzzle = pieces_puzzle.copy()

		pieces_puzzle_gray = cv2.cvtColor(pieces_puzzle, cv2.COLOR_BGR2GRAY)

		_, pieces_puzzle_bw =cv2.threshold(pieces_puzzle_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

		kernel = np.ones((5,5), np.uint8)
		pieces_puzzle_bw_erosion = cv2.erode(pieces_puzzle_bw, kernel, iterations = 2) 


		pieces_puzzle_edges = cv2.Canny(pieces_puzzle_bw_erosion, 100, 200) 


		rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
		pieces_puzzle_edges = cv2.morphologyEx(pieces_puzzle_edges, cv2.MORPH_CLOSE, rect_kernel)


		

		_,contours, hierarchy = cv2.findContours(pieces_puzzle_edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 

		solution_name = self.folder_path+'/SolutionPuzzle.png'


		cv2.imwrite(solution_name,full_puzzle.copy())

		number_contours = len(contours)

		contours_height=[]
		contours_width=[]
		
		for contours_part in contours:
			rect = cv2.boundingRect(contours_part)
			_,_,w,h = rect
			#if h>(400/number_contours)/2 and h<400:
			contours_height.append(h)
			#if w>(600/number_contours)/2 and w<600:
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



	
		contour_cnt = 0
		for contours_part in contours:
						
			countour_list = contours_part.tolist()
			rect = cv2.boundingRect(contours_part)
			x,y,w,h = rect
			if (w<contours_width_lower_bound and w<contours_height_lower_bound)  or (h< contours_width_lower_bound and h<contours_height_lower_bound):
				continue

			if (w>contours_width_upper_bound and w>contours_height_upper_bound)  or (h> contours_width_upper_bound and h>contours_height_upper_bound):
				continue


			contour_cnt+=1
			box = cv2.rectangle(copy_pieces_puzzle, (x,y), (x+w,y+h), (0,0,255), 2)
			cropped = copy_pieces_puzzle[y: y+h, x: x+w]
			part_name = self.folder_path+"/piece"+str(contour_cnt)+".png"
			cv2.imwrite(part_name, cropped)
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
		
		return solution_name

	def feature_matches(self,part_puzzle_name,full_puzzle_name,solution_name,part_number,max_distance):
		try:
			full_puzzle = cv2.imread(full_puzzle_name,0)
			part_puzzle = cv2.imread(part_puzzle_name,0)
			solution_puzzle = cv2.imread(solution_name,1)

			sift = cv2.xfeatures2d.SIFT_create()

			kp1, des1 = sift.detectAndCompute(full_puzzle,None)
			kp2, des2 = sift.detectAndCompute(part_puzzle,None)

			bf = cv2.BFMatcher()
			matches = bf.knnMatch(des1,des2, k=2)

			good = []
			list_points = []
			for m,n in matches:
				if m.distance < 0.65*n.distance:
					img1_idx = m.queryIdx
					x,y = kp1[img1_idx].pt 
					list_points.append((x,y))
					good.append([m])
			
			if not good:
				return False

			print(list_points)
			if (len(list_points)) >1:
				Z = ward(pdist(list_points))
				array = fcluster(Z, t=max_distance, criterion='distance')
			
				counts = np.bincount(array)
				leading_cluster = np.argmax(counts)
			
				leading_cluster_points_idx = np.where(array == leading_cluster)
				leading_cluster_points_idx = (leading_cluster_points_idx[0]).tolist()

				points = itemgetter(*leading_cluster_points_idx)(list_points)
				avg_point_x = mean(value[0] for value in points)
				avg_point_y = mean(value[1] for value in points)
			else:
				avg_point_x = (list_points[0])[0]
				avg_point_y = (list_points[0])[1]


			cv2.putText(solution_puzzle, str(part_number), (int(avg_point_x) , int(avg_point_y) ) , cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0),2,  lineType=cv2.LINE_AA) 
			cv2.imwrite(solution_name,solution_puzzle)
		
			return True
			
		except:
			return False


obj = PuzzleSolution('C:\\Users\\Filip.Dimovski\\Desktop\\test')
obj.solve_puzzle_algorithm()
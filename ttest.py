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
      

 




    def solve_puzzle_algorithm(self):

     
        full_puzzle_name = self.folder_path+'/FullPuzzle.png'
        pieces_puzzle_name = self.folder_path+'/index.jpg'
        
        pieces_puzzle_1 = cv2.imread(pieces_puzzle_name)
        full_puzzle = cv2.imread(full_puzzle_name) 
        pieces_puzzle = cv2.resize(pieces_puzzle_1,(600,400), interpolation = cv2.INTER_AREA) 
        
        copy_pieces_puzzle = pieces_puzzle.copy()
        
        pieces_puzzle_gray = cv2.cvtColor(pieces_puzzle, cv2.COLOR_BGR2GRAY)
        
        _, pieces_puzzle_bw =cv2.threshold(pieces_puzzle_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        
        cv2.imshow('',pieces_puzzle_bw)
        cv2.waitKey()

        kernel_1 =np.ones((3,3), np.uint8) 
        pieces_puzzle_bw_erosion = cv2.dilate(pieces_puzzle_bw, kernel_1, iterations = 2) 

        kernel = np.ones((7,7), np.uint8)
        pieces_puzzle_bw_erosion = cv2.erode(pieces_puzzle_bw_erosion, kernel, iterations = 2) 
        

        cv2.imshow('erozija',pieces_puzzle_bw_erosion)
        cv2.waitKey()
        
        
        pieces_puzzle_edges = cv2.Canny(pieces_puzzle_bw_erosion, 100, 200) 
        
        
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        pieces_puzzle_edges = cv2.morphologyEx(pieces_puzzle_edges, cv2.MORPH_CLOSE, rect_kernel)
        
        
        
        
        _,contours, hierarchy = cv2.findContours(pieces_puzzle_edges,cv2.RETR_EXTERNAL , cv2.CHAIN_APPROX_SIMPLE) 
        
        
        solution_name = self.folder_path+'/SolutionPuzzle.png'
        
        cv2.imwrite(solution_name,full_puzzle.copy())
        
        number_contours = len(contours)

        print( str(number_contours) )

        cv2.drawContours(pieces_puzzle, contours, -1, (0,255,0), 3)
        cv2.imshow('',pieces_puzzle)
        cv2.waitKey()
        
        contours_height=[]
        contours_width=[]
        
        for contours_part in contours:
            rect = cv2.boundingRect(contours_part)
            _,_,w,h = rect
            contours_height.append(h)
            #if w>(600/number_contours)/2 and w<600:
            contours_width.append(w)


        print(contours_height)
        
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
        cont = []
        for contours_part in contours:
          
            countour_list = contours_part.tolist()
            rect = cv2.boundingRect(contours_part)
            x,y,w,h = rect
            if (w<contours_width_lower_bound and w<contours_height_lower_bound)  or (h< contours_width_lower_bound and h<contours_height_lower_bound):
                continue
        
            if (w>contours_width_upper_bound and w>contours_height_upper_bound)  or (h> contours_width_upper_bound and h>contours_height_upper_bound):
                continue
        
            print('w: '+ str(w), ' H:' + str(h))
            cont.append(contours_part)
            
        
        cv2.drawContours(pieces_puzzle, cont, -1, (0,255,0), 3)
        cv2.imshow('',pieces_puzzle)
        cv2.waitKey()

       

      
obj = PuzzleSolution('C:\\Users\\Filip.Dimovski\\Desktop')
obj.solve_puzzle_algorithm()
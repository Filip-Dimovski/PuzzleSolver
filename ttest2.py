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
import matplotlib.image as mpimg

class PuzzleSolution(Widget):
  
    def __init__(self, folder_path_io,**kwa):
        self.folder_path = folder_path_io
      
    def feature_matches(self,part_puzzle_name,full_puzzle_name):
       
        full_puzzle = cv2.imread(full_puzzle_name,0)
        part_puzzle = cv2.imread(part_puzzle_name,0)
     
        sift = cv2.xfeatures2d.SIFT_create()

        max_distance= 104.1393297462587
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

        Z = ward(pdist(list_points))
        array = fcluster(Z, t=max_distance, criterion='distance')
        list_points =  np.array(list_points)
       
        img=mpimg.imread('C:\\Users\\Filip.Dimovski\\Documents\\PuzzleSolver\\users\\0\\teee_20200102_100326\\FullPuzzle.png')
        plt.imshow(img)
        plt.scatter(list_points[array==5, 0], list_points[array==5, 1], s=50, marker='o', color='red')
        plt.scatter(list_points[array==1, 0], list_points[array==1, 1], s=50, marker='o', color='blue')
        plt.scatter(list_points[array==2, 0], list_points[array==2, 1], s=50, marker='o', color='green')
        plt.scatter(list_points[array==3, 0], list_points[array==3, 1], s=50, marker='o', color='purple')
        plt.scatter(list_points[array==4, 0], list_points[array==4, 1], s=50, marker='o', color='orange')
        plt.scatter(list_points[array==6, 0], list_points[array==6, 1], s=50, marker='o', color='yellow')
        plt.scatter(list_points[array==7, 0], list_points[array==7, 1], s=50, marker='o', color='black')
        plt.show()

obj = PuzzleSolution('C:\\Users\\Filip.Dimovski\\Documents\\PuzzleSolver\\users\\0\\teee_20200102_100326')
PuzzleSolution('').feature_matches('C:\\Users\\Filip.Dimovski\\Documents\\PuzzleSolver\\users\\0\\teee_20200102_100326\\piece1.png','C:\\Users\\Filip.Dimovski\\Documents\\PuzzleSolver\\users\\0\\teee_20200102_100326\\FullPuzzle.png')
import random
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction,QLabel,QFileDialog,QTabWidget,QStackedWidget, QDockWidget,QSlider,QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PIL.ImageQt import ImageQt
from PIL import Image

import matplotlib.pyplot as pyplot
import numpy as np
import cv2
import struct
import sys


class SecondWindow(QMainWindow):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        uic.loadUi('secondWindow.ui', self)
        self.setWindowTitle('Spatial Filtering')
        self.img = None
        self.origimg = self.findChild(QLabel, 'origimg')
        self.img1 = self.findChild(QLabel, 'img1')
        self.img1_label = self.findChild(QLabel, 'img1_label')
        self.img2 = self.findChild(QLabel, 'img2')
        self.img2_label = self.findChild(QLabel, 'img2_label')
        self.img3 = self.findChild(QLabel, 'img3')
        self.img3_label = self.findChild(QLabel, 'img3_label')
        self.avgfilter = self.findChild(QPushButton, 'avg_filter')
        self.mdnfilter = self.findChild(QPushButton, 'mdn_filter')
        self.hpassfilter = self.findChild(QPushButton, 'hpass_filter')
        self.unsharpfilter = self.findChild(QPushButton, 'unsharp_filter')
        self.hboostfilter = self.findChild(QPushButton, 'hboost_filter')
        self.sobelgradient = self.findChild(QPushButton, 'sobel_gradient')
        self.salt_pepper = self.findChild(QPushButton, 'salt_pepper')
        self.reset = self.findChild(QPushButton, 'reset_original')
        
        self.avgfilter.clicked.connect(self.sf_avg)
        self.mdnfilter.clicked.connect(self.sf_mdn)
        self.unsharpfilter.clicked.connect(self.sf_unsharp)
        self.sobelgradient.clicked.connect(self.sf_sobel)
        self.hboostfilter.clicked.connect(self.sf_hboost)
        self.hpassfilter.clicked.connect(self.sf_hpass)
        self.salt_pepper.clicked.connect(self.salt_pepper_noise)
        self.reset.clicked.connect(self.reset_image)
    
    def display_info(self,s):
        
        self.img1.clear()
        self.img1_label.setText("")
        self.img2.clear()
        self.img2_label.setText("")
        self.img3.clear()
        self.img3_label.setText("")
        
        img = cv2.imread('dump.png')
        height,width,channel = img.shape
        bytes_pl = 3 * width
        img = QImage(img.data,width,height,bytes_pl,QImage.Format_RGB888)
      
        pixmap = QPixmap.fromImage(img)
        self.origimg.setPixmap(pixmap)
        self.show()
        
    #Reset Image
    def reset_image(self):
        img = cv2.imread('orig.png')
        (row,col) = img.shape[:2]
        for i in range(row):
          for j in range(col):
            img[i,j] = sum(img[i,j])/3
        height,width,channel = img.shape
        bytes_pl = 3 * width
        img = QImage(img.data,width,height,bytes_pl,QImage.Format_RGB888)
        img.save('dump.png')
        pixmap = QPixmap.fromImage(img)
        self.origimg.setPixmap(pixmap)
    
    def salt_pepper_noise(self):
        img = cv2.imread('dump.png')
        (row,col) = img.shape[:2]
        n_pixels = random.randint(300,10000)
        for i in range(n_pixels):
          x = random.randint(0,row-1)
          y = random.randint(0,col-1)
          img[x,y] = 0
        n_pixels = random.randint(300,10000)
        for i in range(n_pixels):
          x = random.randint(0,row-1)
          y = random.randint(0,col-1)
          img[x,y] = 255
        height,width,channel = img.shape
        bytes_pl = 3 * width
        img = QImage(img.data,width,height,bytes_pl,QImage.Format_RGB888)
        img.save('dump.png')
        pixmap = QPixmap.fromImage(img)
        self.origimg.setPixmap(pixmap)
        
          
   #Spatial Filtering - Averaging Filter
    def sf_avg(self,s):
        img = cv2.imread('dump.png')
        kernel = np.array([[1,2,1],[2,4,2],[1,2,1]])
        kernel = kernel/16
        img = cv2.filter2D(img,-1,kernel)
        height,width,channel = img.shape
        bytes_pl = 3 * width
        img = QImage(img.data,width,height,bytes_pl,QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(img)
        self.img1.setPixmap(pixmap)

     #Spatial Filtering - Median Filter
    def sf_mdn(self,s):
          img = cv2.imread('dump.png')
          (row,col) = img.shape[:2]
          for i in range(row-2):
            for j in range(col-2):
              temp = []
              for k in range(3):
                for l in range(3):
                  temp.append(sum(img[i+k,j+l])/3)
              temp.sort()
              img[i+1,j+1] = temp[4]
          height,width,channel = img.shape
          bytes_pl = 3 * width
          img = QImage(img.data,width,height,bytes_pl,QImage.Format_RGB888)
          pixmap = QPixmap.fromImage(img)
          self.img1.setPixmap(pixmap)

    
    #Unsharp Masking
    def sf_unsharp(self,s):
          img = cv2.imread('dump.png')
          blur = img.copy()
          kernel = np.ones((3,3),np.float32)/9
          blur = cv2.filter2D(blur,-1,kernel)
          mask = img - blur
          sharp = img + mask
          height,width,channel = sharp.shape
          bytes_pl = 3 * width
          img = QImage(sharp.data,width,height,bytes_pl,QImage.Format_RGB888)
          pixmap = QPixmap.fromImage(img)
          self.img1.setPixmap(pixmap)

  
  #Highpass Filter Laplacian Operator
    def sf_hpass(self):
          img = cv2.imread('dump.png')
          kernel = np.array([[0,-1,0],[-1,4,-1],[0,-1,0]])
          img = cv2.filter2D(img,-1,kernel)
          
          height,width,channel = img.shape
          bytes_pl = 3 * width
          img = QImage(img.data,width,height,bytes_pl,QImage.Format_RGB888)
          pixmap = QPixmap.fromImage(img)
          self.img1.setPixmap(pixmap)

  #Highboost Filtering
    def sf_hboost(self):
          img = cv2.imread('dump.png')
          blur = img.copy()
          kernel = np.ones((3,3),np.float32)/9
          blur = cv2.filter2D(blur,-1,kernel)
          mask = img + 5 - blur
          
          height,width,channel = mask.shape
          bytes_pl = 3 * width
          img = QImage(mask.data,width,height,bytes_pl,QImage.Format_RGB888)
          pixmap = QPixmap.fromImage(img)
          self.img1.setPixmap(pixmap)
  
  #Sobel Edge Detection
    def sf_sobel(self):
          img = cv2.imread('dump.png')
          
          xkernel = np.array([[-1,-2,-1],
                              [0,0,0],
                              [1,2,1]])
          ykernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
          xsobel = cv2.filter2D(img,-1,xkernel)
          ysobel = cv2.filter2D(img,-1,ykernel)
          
       
          
          magnitude = np.abs(xsobel) + np.abs(ysobel)
        
          
          ximg = Image.fromarray(xsobel.astype(np.uint8)).resize((400,400))
          yimg = Image.fromarray(ysobel.astype(np.uint8)).resize((400,400))
          final_img = Image.fromarray((magnitude).astype(np.uint8)).resize((400,400))
          
          t_x = ImageQt(ximg)
          t_y = ImageQt(yimg)
          t_f = ImageQt(final_img)
          q_x = QImage(t_x)
          p_x = QPixmap.fromImage(q_x)
          p_y = QPixmap.fromImage(t_y)
          p_f = QPixmap.fromImage(t_f)
          self.img1.setPixmap(p_x)
          self.img1_label.setText('X-Sobel')
          self.img2.setPixmap(p_y)
          self.img2_label.setText('Y-Sobel')
          self.img3.setPixmap(p_f)
          self.img3_label.setText('Magnitude')
    
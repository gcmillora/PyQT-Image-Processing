#CMSC162: Activity 4 - Image Enhancement Basics
#Author: Greg Norman C. Millora (2019-60019)
#Date: 10/13/2022

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction,QLabel,QFileDialog,QTabWidget,QStackedWidget, QDockWidget,QSlider,QPushButton
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PIL.ImageQt import ImageQt
from PIL import Image
from cv2 import QT_PUSH_BUTTON
import matplotlib.pyplot as pyplot
import numpy as np
import cv2
import struct
import sys



#Class for PCX Information
class PCX():
  #Function to open and read PCX file
  def open_pcx(self,path):
      with open(f'{path}','rb') as pcx:
          self.manufacturer = struct.unpack('B', pcx.read(1))[0]
          self.ver = struct.unpack('B', pcx.read(1))[0]
          self.encd = struct.unpack('B', pcx.read(1))[0]
          self.bits = struct.unpack('B', pcx.read(1))[0]
          self.xmin = struct.unpack('H', pcx.read(2))[0]
          self.ymin = struct.unpack('H', pcx.read(2))[0]
          self.xmax = struct.unpack('H', pcx.read(2))[0]
          self.ymax = struct.unpack('H', pcx.read(2))[0]
          self.hdpi = struct.unpack('H', pcx.read(2))[0]
          self.vdpi = struct.unpack('H', pcx.read(2))[0]
          pcx.seek(65,0)
          self.planes = struct.unpack('B', pcx.read(1))[0]
          self.bytes = struct.unpack('H', pcx.read(2))[0]
          self.palette= struct.unpack('H', pcx.read(2))[0]
          self.hor_ss = struct.unpack('H', pcx.read(2))[0]
          self.vert_ss = struct.unpack('H', pcx.read(2))[0]


#Class for Main Window
class UI(QMainWindow, PCX):
  def __init__(self):
    #Load the UI from QtDesigner
    super(UI, self).__init__()
    uic.loadUi('viewer.ui', self)
    self.show()
    

    
    #Declare the objects and find QObjects from UI
    self.button = self.findChild(QAction, 'actionAdd_Image')
    self.label = self.findChild(QLabel, 'image_view')
    self.information = self.findChild(QLabel, 'img_info')
    self.plotLabel = self.findChild(QLabel, 'plotLabel')
    self.getRedChannel = self.findChild(QAction,'getRed')
    self.getBlueChannel = self.findChild(QAction,'getBlue')
    self.getGreenChannel = self.findChild(QAction,'getGreen')
    self.grayscale = self.findChild(QAction,'tfGrayscale')
    self.negative = self.findChild(QAction, 'tfNegative')
    self.infoTab = self.findChild(QTabWidget,'infoTab')
    
    #Gamma Dock Widgets
    self.gammaDock = self.findChild(QDockWidget,'gammaDock')
    self.gammaThresh = self.findChild(QAction,'thGamma')
    self.gammaSlider = self.findChild(QSlider,'gammaSlider')
    self.gammaVal = self.findChild(QLabel,'gammaVal')
    self.gammaDock.setHidden(True)
    
    #Black and White Dock Widgets
    self.bnwDock = self.findChild(QDockWidget,'bnwDock')
    self.bnwThresh = self.findChild(QAction,'bnwButton')
    self.bnwSlider = self.findChild(QSlider,'bnwSlider')
    self.bnwVal = self.findChild(QLabel,'bnwVal')
    
    #Utility Widgets
    self.saveImgBNW = self.findChild(QPushButton,'saveImage')
    self.saveImgGamma = self.findChild(QPushButton,'saveImage_2')
    self.reset = self.findChild(QAction,'reset')
    self.grayscaleTool = self.findChild(QAction,'grayscaleTool')
    
    #Initial states of the UI
    self.bnwDock.setHidden(True)
    self.bnwThresh.setEnabled(False)
    self.infoTab.setHidden(True)

    #Connect the buttons to their respective functions
    self.button.triggered.connect(self.add_image)
    self.getRedChannel.triggered.connect(self.split_red)
    self.getBlueChannel.triggered.connect(self.split_blue)
    self.getGreenChannel.triggered.connect(self.split_green)
    self.grayscale.triggered.connect(self.tf_grayscale)
    self.negative.triggered.connect(self.tf_negative)
    self.gammaThresh.triggered.connect(self.show_gamma)
    self.gammaSlider.valueChanged.connect(self.tf_gamma)
    self.bnwThresh.triggered.connect(self.show_bnw)
    self.bnwSlider.valueChanged.connect(self.tf_bnw)
    self.saveImgBNW.clicked.connect(self.save_image)
    self.saveImgGamma.clicked.connect(self.save_image)
    self.reset.triggered.connect(self.reset_image)
    self.grayscaleTool.triggered.connect(self.tf_grayscale)
    
    #Declare the variables
    self.fileopen=''
    self.image = None
    self.orig_img = None
  
  
  def reset_image(self):
    self.bnwSlider.setValue(127)
    self.gammaSlider.setValue(1)
    self.image = self.orig_img
    self.image.save('dump.png')
    self.label.setPixmap(QPixmap.fromImage(ImageQt(self.image)))
    self.gammaDock.setHidden(True)
    self.bnwDock.setHidden(True)
    self.bnwThresh.setEnabled(False)
    
  #Function to show the information tab on the UI
  def show_channel(self):
    self.infoTab.setHidden(False)
  def show_gamma(self):
    self.gammaDock.setHidden(False)
  def show_bnw(self):
    self.bnwDock.setHidden(False)
  
  def save_image(self):
    self.image.save('dump.png')

  #Function to convert an image to PNG and save it to the current directory as 'dump.png'
  def convert_to_png(self,path):
    img = Image.open(self.fileopen)
    img.save('dump.png')
  
  #Function to create a histogram using matplotlib and show to the UI by
  #converting the plot to a .PNG file and setting it to the label.
  def create_histogram(self,histo_values,name):
    pyplot.clf()
    color_y = histo_values
    x = np.arange(0,256)
    print(x)
    
    figure = pyplot.Figure(figsize = (5,5),dpi=80)
    
    pyplot.plot(x, color_y, color=name)
    pyplot.savefig('histo_plot.png')
    plot = Image.open('histo_plot.png')
    plot = plot.resize((500,500))
    temp_img = ImageQt(plot)
    pixmap = QPixmap.fromImage(temp_img)
    self.plotLabel.setPixmap(pixmap)

  #Functions to split the channels of the image and show it to the UI.
  #Also creates a histogram of the channel and shows it to the UI.
  #The histogram is created by using the PIL.Image.histogram() function.
  #Image.merge() is used to merge the channels to create a new image.
  def split_red(self):
    img = Image.open('dump.png')
    img = img.resize((300,300))
    img = img.convert('RGB')
    
    red, green, blue = img.split()
    histogram = red.histogram()
    channel = Image.merge('RGB', (red, red.point(lambda _:0),red.point(lambda _:0)))
    self.create_histogram(histogram,'RED')
    self.show_image(channel)
    
  def split_green(self):
    img = Image.open('dump.png')
    img = img.resize((300,300))
    img = img.convert('RGB')
    
    red, green, blue = img.split()
    histogram = green.histogram()
    channel = Image.merge('RGB', (green.point(lambda _:0), green, green.point(lambda _:0)))
    self.create_histogram(histogram,'GREEN')
    self.show_image(channel)
    
  def split_blue(self):
    img = Image.open('dump.png')
    img = img.resize((300,300))
    img = img.convert('RGB')
    
    red,green,blue = img.split()
    histogram = blue.histogram()
    channel = Image.merge('RGB', (blue.point(lambda _:0), blue.point(lambda _:0), blue))
    self.create_histogram(histogram,'BLUE')
    self.show_image(channel)
  
  #Function to transform the image to grayscale using
  #OpenCV. Gets the sum of the RGB pixel values and gets
  #its average and assign it to that pixel. Then convert
  #the image back to PIL Image format from the OpenCV
  #array object.
  
  def tf_grayscale(self):
    img = cv2.imread('dump.png')
    (row,col) = img.shape[:2]
    for i in range(row):
      for j in range(col):
        img[i, j] = sum(img[i, j]) / 3
    img = Image.fromarray(img)
    img.save('dump.png')
    self.show_image(img)
    self.bnwThresh.setEnabled(True)
  
  #Function to transform the image to negative using
  #OpenCV. Gets the sum of the RGB pixel values and subtracts
  #it from 255 and assign it to that pixel. Then convert
  #the image back to PIL Image format from the OpenCV
  #array object.
  def tf_negative(self):
    img = cv2.imread('dump.png')
    (row,col) = img.shape[:2]
    for i in range(row):
      for j in range(col):
        img[i, j] = 255 - img[i, j]
    img = Image.fromarray(img)
    img.save('dump.png')
    self.show_image(img)
    self.bnwThresh.setEnabled(False)
  
  #Function to transform the image to gamma using
  #OpenCV. Gets the sum of the RGB pixel values and
  #raise it to the power of the gamma value and assign
  #it to that pixel. Then convert the image back to PIL
  #Image format from the OpenCV array object.
  def tf_gamma(self, gamma=1.0):
    gamma = gamma/10
    self.gammaVal.setText("Gamma = "+str(gamma))
    image = cv2.imread('dump.png')
    pixel = np.array([((per / 255.0) ** (gamma)) * 255
      for per in np.arange(0, 256)]).astype("uint8")
    img = Image.fromarray(cv2.LUT(image, pixel))
    self.image = img
    self.show_image(img)
  
  #Function to transform the image to black and white using
  #OpenCV. Gets the sum of the RGB pixel values and
  #if the sum is greater than the threshold value, it
  #assigns 255 to that pixel. Else, it assigns 0 to that
  #pixel. Then convert the image back to PIL Image format
  #from the OpenCV array object.
  def tf_bnw(self, k=127.0):
    self.tf_grayscale()
    self.bnwVal.setText("Value = "+str(k))
    img = cv2.imread('dump.png')
    (row,col) = img.shape[:2]
    for i in range(row):
      for j in range(col):
        if sum(img[i,j])/3 < k:
          img[i,j] = 0
        else:
          img[i,j] = 255
    img = Image.fromarray(img)
    self.image = img
    self.show_image(img)
    
  #Function to show the image to the UI
  #Converts the image to a .PNG file and sets it to the label
  #with the size 400x400.
  def show_image(self,img):
    img = img.resize((400,400))
    temp_img = ImageQt(img)
    self.pixmap = QPixmap.fromImage(temp_img)
    self.label.setPixmap(self.pixmap)
    
  def add_image(self,s):
    #If a file was open, clear the plot label and set the text to select channel.
    if(self.fileopen):
      self.plotLabel.clear()
      self.plotLabel.setText("Please select channel to show")
    self.show_channel() #Show the information tab
    self.fileopen,_ = QFileDialog.getOpenFileName(self, 'Open file', '/home',"Image files (*.jpg *.gif *.png *.bmp  *.pcx)")
    
    #Convert the image file to PNG.
    self.convert_to_png(self.fileopen)
    
    #Open the PCX image file and read the header.
    if(self.fileopen.endswith('.pcx')):
      self.open_pcx(self.fileopen)
      self.information.setText(f"Manufacturer: {self.manufacturer} \nVersion: {self.ver} \nEncoding: {self.encd} \nBits per pixel: {self.bits} \nImage Dimensions: {self.xmin} {self.ymin} {self.xmax} {self.ymax} \nHDPI: {self.hdpi} \nVDPI: {self.vdpi} \nNumber of Color Planes: {self.planes} \nBits per Line: {self.bytes} \nPalette Information: {self.palette} \nHorizontal Screen Size: {self.hor_ss} \nVertical Screen Size: {self.vert_ss}")
    else:
      self.information.setText("No Information")
      
    #Open the image file and show it to the UI.
    img = Image.open(self.fileopen)
    self.orig_img = img
    self.show_image(img)
    print(self.fileopen)
    

app = QApplication(sys.argv)
UIWindow = UI()
UIWindow.setWindowTitle('Image Viewer')
app.exec_()
    
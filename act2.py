from PyQt5.QtWidgets import QMainWindow, QApplication, QAction,QLabel,QFileDialog,QTabWidget,QStackedWidget
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
from PIL.ImageQt import ImageQt
from PIL import Image
import matplotlib.pyplot as pyplot
import numpy as np
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
    self.infoTab = self.findChild(QTabWidget,'infoTab')
    self.infoTab.setHidden(True)

    #When self.button is clicked, trigger the function 'add_image()'
    self.button.triggered.connect(self.add_image)
    self.getRedChannel.triggered.connect(self.split_red)
    self.getBlueChannel.triggered.connect(self.split_blue)
    self.getGreenChannel.triggered.connect(self.split_green)
   
    self.fileopen=''
  def show_channel(self):
    self.infoTab.setHidden(False)
    
  def convert_to_png(self,path):
    img = Image.open(self.fileopen)
    img.save('dump.png')
  
  def create_histogram(self,histo_values,name):
    color_y = histo_values
    x = np.arange(0,256)
    print(x)
    
    figure = pyplot.Figure(figsize = (5,5),dpi=80)
    
    pyplot.plot(x, color_y, color=name)

    pyplot.show()
    pyplot.savefig('histo_plot.png')
    plot = Image.open('histo_plot.png')
    plot = plot.resize((500,500))
    temp_img = ImageQt(plot)
    pixmap = QPixmap.fromImage(temp_img)
    self.plotLabel.setPixmap(pixmap)

    
    
  #Function to open a file dialogue and set the selected image to
  #the label using Pixmap
  def split_red(self):
    img = Image.open('dump.png')
    img = img.resize((300,300))
    img = img.convert('RGB')
    red, green, blue = img.split()
    red_channel = Image.merge('RGB', (red, red.point(lambda _:0),red.point(lambda _:0)))
    red_histogram = red.histogram()
    self.create_histogram(red_histogram,'RED')
    print(red_histogram)
    self.show_image(red_channel)
    
  def split_green(self):
    img = Image.open('dump.png')
    img = img.resize((300,300))
    img = img.convert('RGB')
    
    red, green, blue = img.split()
    green_channel = Image.merge('RGB', (green.point(lambda _:0), green, green.point(lambda _:0)))
    green_histogram = green.histogram()
    self.create_histogram(green_histogram,'GREEN')
    print(green_histogram)
    self.show_image(green_channel)
    
  def split_blue(self):
    img = Image.open('dump.png')
    img = img.resize((300,300))
    img = img.convert('RGB')
    
    red,green,blue = img.split()
    blue_channel = Image.merge('RGB', (blue.point(lambda _:0), blue.point(lambda _:0), blue))
    blue_histogram = blue.histogram()
    self.create_histogram(blue_histogram,'BLUE')
    print(blue_histogram)
    self.show_image(blue_channel)
    
  def show_image(self,img):
    img = img.resize((400,400))
    temp_img = ImageQt(img)
    self.pixmap = QPixmap.fromImage(temp_img)
    self.label.setPixmap(self.pixmap)
    
  def add_image(self,s):
    
    if(self.fileopen):
      self.plotLabel.clear()
      self.plotLabel.setText("Please select channel to show")
    self.show_channel()
    self.fileopen,_ = QFileDialog.getOpenFileName(self, 'Open file', '/home',"Image files (*.jpg *.gif *.png *.bmp  *.pcx)")
    self.convert_to_png(self.fileopen)
    
    
    if(self.fileopen.endswith('.pcx')):
      self.open_pcx(self.fileopen)
      self.information.setText(f"Manufacturer: {self.manufacturer} \nVersion: {self.ver} \nEncoding: {self.encd} \nBits per pixel: {self.bits} \nImage Dimensions: {self.xmin} {self.ymin} {self.xmax} {self.ymax} \nHDPI: {self.hdpi} \nVDPI: {self.vdpi} \nNumber of Color Planes: {self.planes} \nBits per Line: {self.bytes} \nPalette Information: {self.palette} \nHorizontal Screen Size: {self.hor_ss} \nVertical Screen Size: {self.vert_ss}")
    else:
      self.information.setText("No Information")
    self.image = Image.open(self.fileopen)
    self.show_image(self.image)
    print(self.fileopen)
    
 

app = QApplication(sys.argv)
UIWindow = UI()
UIWindow.setWindowTitle('Image Viewer')
app.exec_()
    
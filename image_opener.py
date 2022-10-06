#import necessary modules
import io
from PIL import Image

#function to display the Image
# also it displays RGB channel with its corresponding histogram
def image_opens(filename,window):
    image = Image.open(filename) #open file path of image
    image.thumbnail((300, 300)) #max size of picture in the app
    bio = io.BytesIO() #stores image
    image.save(bio, format="PNG") #save to png file to open the image

    red = Image.open('C:/Users/Murky/Downloads/162_image_test/part3/red.png') #open file path of image
    red.thumbnail((300, 300))
    red1 = io.BytesIO() #stores image
    red.save(red1, format="PNG")

    blue = Image.open('C:/Users/Murky/Downloads/162_image_test/part3/blue.png') #open file path of image
    blue.thumbnail((300, 300))#max size of picture in the app
    blue1 = io.BytesIO() #stores image
    blue.save(blue1, format="PNG")#save to png file to open the image

    green = Image.open(
        'C:/Users/Murky/Downloads/162_image_test/part3/green.png') #open file path of image
    green.thumbnail((300, 300))#max size of picture in the app
    green1 = io.BytesIO() #stores image
    green.save(green1, format="PNG")#save to png file to open the image

    reds_graph = Image.open(
        'C:/Users/Murky/Downloads/162_image_test/part3/red_graph.png') #open file path of image
    reds_graph.thumbnail((400, 400))#max size of picture in the app
    red_graph = io.BytesIO() #stores image
    reds_graph.save(red_graph, format="PNG")#save to png file to open the image

    blues_graph = Image.open(
        'C:/Users/Murky/Downloads/162_image_test/part3/blue_graph.png') #open file path of image
    blues_graph.thumbnail((400, 400))#max size of picture in the app
    blue_graph = io.BytesIO() #stores image
    blues_graph.save(blue_graph, format="PNG")#save to png file to open the image

    greens_graph = Image.open(
        'C:/Users/Murky/Downloads/162_image_test/part3/green_graph.png') #open file path of image
    greens_graph.thumbnail((400, 400))#max size of picture in the app
    green_graph = io.BytesIO() #stores image
    greens_graph.save(green_graph, format="PNG")#save to png file to open the image
    
    
    #Opens the image in the window/GUI
    window["-IMAGE-"].update(data=bio.getvalue())
    window["-red_image-"].update(data=red1.getvalue())
    window["-red_image_graph-"].update(
        data=red_graph.getvalue())
    window["-blue_image-"].update(data=blue1.getvalue())
    window["-blue_image_graph-"].update(
        data=blue_graph.getvalue())
    window["-green_image-"].update(data=green1.getvalue())
    window["-green_image_graph-"].update(
        data=green_graph.getvalue())

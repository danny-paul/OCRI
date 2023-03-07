#from https://deepnote.com/@davidespalla/Recognizing-handwriting-with-Tensorflow-and-OpenCV-cfc4acf5-188e-4d3b-bdb5-a13aa463d2b0

from keras.models import load_model
from PIL import Image
import tensorflow as tf
import cv2
import matplotlib.pyplot as plt
import numpy as np

import imutils
from imutils.contours import sort_contours

from matplotlib import cm

import os

from collections import defaultdict

def recognize():
    crop1 = 50
    crop2 = 1000
    crop3 = 50
    crop4 = 2500

    #loads the model with the keras load_model function
    model_path = os.getcwd() + '\\Image_Recognition\\model_v3\\'
    print("Loading NN model...")
    model = load_model(model_path)
    print("Done")

    #image_path = 'handwriting_example1_resized.png'
    image_filename = 'ciltest2.png'
    image_path = os.getcwd() + '\\Image_Recognition\\Images\\'
    image = cv2.imread(image_path + image_filename)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cropped = gray[crop1:crop2, crop3:crop4]
    blurred = cv2.GaussianBlur(cropped, (5, 5), 0)

    #for testing
    #showImages(image, gray, cropped)

    #convert cv2 to pil
    blurred = Image.fromarray(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
    pixelMap = blurred.load()

    avgColor = 0
    pixelCount = 0

    #find average color
    w, h = blurred.size
    for i in range(w):
        for j in range(h):
            b, g, r = blurred.getpixel((i, j))
            avgColor = (b + g + r)/3 + avgColor
            pixelCount = pixelCount + 1

    avgColor = avgColor / pixelCount
            
    #convert to pure black and white
    w, h = blurred.size
    for i in range(w):
        for j in range(h):
            b, g, r = blurred.getpixel((i, j))
            if (r + b + g)/3 < avgColor - 10:
                pixelMap[i, j] = (0, 0, 0)
            else:
                pixelMap[i, j] = (255, 255, 255)

    blurred = np.array(blurred)
    blurred = blurred[:, :, ::-1].copy()

    #plt.imshow(blurred,cmap=cm.binary_r)
    #plt.show()      #testing, show images used for recognition

    #perform edge detection, find contours in the edge map, and sort the
    #resulting contours from left-to-right
    edged = cv2.Canny(blurred, 30, 250) #low_threshold, high_threshold
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to_right")[0]

    figure = plt.figure(figsize=(7,7))
    plt.axis('off');
    plt.imshow(edged,cmap=cm.binary_r);

    chars = []
    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and isolate ROI
        (x, y, w, h) = cv2.boundingRect(c)
        roi = cropped[y:y + h, x:x + w]
      
        #binarize image, finds threshold with OTSU method
        thresh = cv2.threshold(roi, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
      
        # resize largest dimension to input size
        (tH, tW) = thresh.shape
        #print('tH', tH)
        #print('tW', tW)
        if tW / tH < 28 and tH / tW < 28:  #for propper dimensions, no abnormally long or tall images
            if tW > tH:
                thresh = imutils.resize(thresh, width=28)
            # otherwise, resize along the height
            else:
                thresh = imutils.resize(thresh, height=28)

        # find how much is needed to pad
        (tH, tW) = thresh.shape
        dX = int(max(0, 28 - tW) / 2.0)
        dY = int(max(0, 28 - tH) / 2.0)
        # pad the image and force 28 x 28 dimensions
        padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
        left=dX, right=dX, borderType=cv2.BORDER_CONSTANT,
        value=(0, 0, 0))
        padded = cv2.resize(padded, (28, 28))
        # reshape and rescale padded image for the model
        padded = padded.astype("float32") / 255.0
        padded = np.expand_dims(padded, axis=-1)
        # append image and bounding box data in char list
        chars.append((padded, (x, y, w, h)))

    # plot isolated characters
    n_cols = 10
    n_rows = int(np.floor(len(chars)/ n_cols)+1)
    fig = plt.figure(figsize=(1.5*n_cols,1.5*n_rows))
    for i,char in enumerate(chars):
        ax = plt.subplot(n_rows,n_cols,i+1)
        ax.imshow(char[0][:,:,0],cmap=cm.binary,aspect='auto')
        #plt.axis('off')
    plt.tight_layout()
    #plt.show()

    boxes = [b[1] for b in chars]
    chars = np.array([c[0] for c in chars], dtype="float32")
    #OCR the characters using our handwriting recognition model
    preds = model.predict(chars)
    #define the list of label names
    labelNames = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt"

    image = cv2.imread(image_path + image_filename)
    cropped = image[crop1:crop2,crop3:crop4]
    cropped2 = np.copy(cropped)     #cropped 2 will omit characters, to detect lines

    #recognize letters letter
    letterBoxes = []
    for (pred, (x, y, w, h)) in zip(preds, boxes):
        pred = modifyPreds(pred)    #only use certain characters
        
        #find the index of the label with the largest corresponding
        #probability, then extract the probability and label
        i = np.argmax(pred)
        prob = pred[i]
        label = labelNames[i]
        #draw the prediction on the image and it's probability
        label_text = f"{label}, {prob * 100:.1f}%"
        if (prob >= .7) and (w > 10) and (h > 10) and (h/w < 5) and (w/h < 5):
            cv2.rectangle(cropped, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.rectangle(cropped2, (x, y), (x + w, y + h), (255, 255, 255), -1)
            cv2.putText(cropped, label_text, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            letterBoxes.append((x, y, w, h, label))

    #save the images to open them up with cv2 library
    plt.figure(figsize=(15,10))
    plt.imshow(cropped)
    plt.savefig(image_path + 'WithChars.png')
    plt.imshow(cropped2)
    plt.savefig(image_path + 'NoChars.png')
    #plt.show()

    #close and reopen the image
    WithChars = cv2.imread(image_path + 'WithChars.png')
    NoChars = cv2.imread(image_path + 'NoChars.png', 0)

    #line segment detection
    #from https://stackoverflow.com/questions/41329665/linesegmentdetector-in-opencv-3-with-python

    #create default parametrization LSD
    lsd = cv2.createLineSegmentDetector(0)  #find out what 0 means

    #Detect lines in the image
    lines = lsd.detect(NoChars)[0] #position 0 of the retuned tuple are the detected lines

    #draw detected lines in the image
    lineImage = lsd.drawSegments(WithChars, lines)

    #Show image
    #cv2.imshow("LSD", lineImage)
    #plt.show()

    return letterBoxes, lines

#modify odds of certain characters
def modifyPreds(pred):
    labelNames = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt"

    i = np.argmax(pred)

    #table of characters to modify
    pred[0] = 0                 #0
    pred[1] = pred[1]           #1
    pred[2] = pred[2]           #2
    pred[3] = pred[3]           #3
    pred[4] = pred[4]           #4
    pred[5] = pred[5]           #5
    pred[6] = pred[6]           #6
    pred[7] = pred[7]           #7
    pred[8] = pred[8]           #8
    pred[9] = pred[9]           #9
    pred[10] = pred[10]         #A
    pred[11] = pred[11]         #B
    pred[12] = pred[12] + .15   #C  is common
    pred[13] = 0                #D  not used
    pred[14] = 0                #E  not used
    pred[15] = pred[15]         #F
    pred[16] = 0                #G  not used
    pred[17] = pred[17] + .15   #H  is common
    pred[18] = 0                #I  not used
    pred[19] = 0                #J  not used
    pred[20] = pred[20]         #K
    pred[21] = pred[21]         #L
    pred[22] = pred[22]         #M
    pred[23] = pred[23] + .15   #N` is common
    pred[24] = pred[24] + .15   #O  is common
    pred[25] = pred[25]         #P
    pred[26] = 0                #Q  not used
    pred[27] = pred[27]         #R
    pred[28] = pred[28]         #S
    pred[29] = 0                #T
    pred[30] = 0                #U
    pred[31] = 0                #V
    pred[32] = 0                #W
    pred[33] = 0                #X
    pred[34] = 0                #Y
    pred[35] = 0                #Z
    pred[36] = pred[36]         #a
    pred[37] = pred[37]         #b
    pred[38] = 0                #d  not used
    pred[39] = pred[39]         #e
    pred[40] = 0                #f
    pred[41] = pred[41]         #g
    pred[42] = 0                #h  not used
    pred[43] = pred[43]         #n
    pred[44] = 0                #q  not used
    pred[45] = pred[45]         #r
    pred[46] = pred[46]         #t

    if np.argmax(pred) == 24:           #O needs extra help
        pred[24] = pred[24] + 1

    return pred


#testing function
def showImages(image, gray, cropped):
    #%matplotlib inline #for Jupyter IPython notebook only
    fig = plt.figure(figsize=(12,4))
    ax = plt.subplot(1,4,1)
    ax.imshow(image)
    ax.set_title('original image');

    ax = plt.subplot(1,4,2)
    ax.imshow(gray,cmap=cm.binary_r)
    ax.set_axis_off()
    ax.set_title('grayscale image');

    #crop the image: we has to be a custom crop for each image
    ax = plt.subplot(1,4,3)
    ax.imshow(cropped,cmap=cm.binary_r)
    ax.set_axis_off()
    ax.set_title('cropped image');

    plt.show()

# takes list of lines and reduces them to the absolute necessary values
def process_lines():
    print()


class mapped_node:
    def __init__(self, type_is: str, x: int, y: int, width: int, height: int):
        self.type = type_is
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.associated_edges = list[mapped_edge]
        

class mapped_edge:
    def __init__(self, list_of_lines: list[tuple, tuple], type_is= "unknown"):
        self.list_of_lines = list_of_lines
        self.type = type_is
        self.avg_coordinate_line_start: tuple = self.calc_avg_line_start()
        self.avg_coordinate_line_end: tuple = self.calc_avg_line_end()
    
    def calc_avg_line_start(self):
        line_start_tuple = (2, 2)
        return line_start_tuple
    
    def calc_avg_line_end(self):
        line_end_tuple = (4, 4)
        return line_end_tuple
    
    def determine_type(self):
        return "Single Bond"
            

class edge_map:
    def __init__(self, edge_list = list[mapped_edge], edgeless_nodes = list[mapped_node]):
        self.graph = defaultdict(set) # key = edge, value = set of atoms (2)
        self.edge_list = edge_list
        self.edgeless_nodes = edgeless_nodes
            
    def add_edge(self, edge: mapped_edge):
        print()
        
    def associate_node_with_edge(self, edge: mapped_edge):
        print()
            


                        

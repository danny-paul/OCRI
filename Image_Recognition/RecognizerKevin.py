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
import math

import os

def recognize():
	crop1 = 0
	crop2 = 1000
	crop3 = 0
	crop4 = 3000

	#loads the model with the keras load_model function
	model_path = os.getcwd() + '\\Image_Recognition\\model_v3\\'
	print("Loading NN model...")
	model = load_model(model_path)
	print("Done")
    
	image_filename = 'PenTest2.png'
	image_path = os.getcwd() + '\\Image_Recognition\\Images\\'
	image = cv2.imread(image_path + image_filename)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	cropped = gray[crop1:crop2, crop3:crop4]
	blurred = cv2.GaussianBlur(cropped, (5, 5), 0)

    #for testing
    #showImages(image, gray, cropped)

    #convert to pure black and white
	blurred = pureBlackWhite(blurred)

    #plt.imshow(blurred,cmap=cm.binary_r)
    #plt.show()      #testing, show images used for recognition

    #perform edge detection, find contours in the edge map, and sort the
    #resulting contours from left-to-right
	edged = cv2.Canny(blurred, 30, 250) # low_threshold, high_threshold
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
		plt.axis('off')
	plt.tight_layout()
	#plt.show()

	boxes = [b[1] for b in chars]
	chars = np.array([c[0] for c in chars], dtype="float32")
	#OCR the characters using our handwriting recognition model
	preds = model.predict(chars)
	#define the list of label names
	labelNames = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabdefghnqrt"

	image = cv2.imread(image_path + image_filename)
	grayImage = cv2.imread(image_path + image_filename, 0)   #important for line segment detection
	cropped = image[crop1:crop2,crop3:crop4]
	cropped2 = grayImage[crop1:crop2,crop3:crop4]     #cropped 2 will omit characters, to detect lines

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

	WithChars = cropped     #image with characters, used for printing
	NoChars = cropped2      #image without characters, used for line segment detection

	NoChars = cv2.GaussianBlur(NoChars, (5, 5), 0)
	#NoChars = pureBlackWhite(NoChars)

	#line segment detection
	#from https://stackoverflow.com/questions/41329665/linesegmentdetector-in-opencv-3-with-python

	#create default parametrization LSD
	lsd = cv2.createLineSegmentDetector(0)  #find out what 0 means

	#Detect lines in the image
	lines = lsd.detect(NoChars)[0] #position 0 of the retuned tuple are the detected lines

	cv2.imshow("LSD input image", NoChars)

	#get rid of unnessessary lines
	avgW, avgH = avgWH(letterBoxes)
	avgSquare = (avgW + avgH)/2
	lines = condenseLines(lines, avgSquare)

	print(letterBoxes[0])



	#testing below vvvvv
	print(lines)

	for i in range(len(lines)):
		X1, Y1, X2, Y2 = lines[i]
		print(X1, Y1, X2, Y2)
		WithChars = cv2.line(WithChars, (int(X1), int(Y1)), (int(X2), int(Y2)), (255, 0, 0), 2)

	#draw detected lines in the image
	#lineImage = lsd.drawSegments(WithChars, lines)  only if the lines aren't condensed

	lengthBoxes = len(letterBoxes)

	#Show image
	letterBoxes2, edgeList = mapEdges(letterBoxes, lines)
	#print dummy carbons
	for i in range(len(letterBoxes2)):
		x, y, w, h, l = letterBoxes2[i]
		cv2.rectangle(WithChars, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 255), 2)
	cv2.imshow("LSD", WithChars)
	#plt.show()
	#testing above ^^^^^^^^^


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

#convert an image to pure black and white
def pureBlackWhite(picture):
    
    #convert cv2 to pil 
    picture = Image.fromarray(cv2.cvtColor(picture, cv2.COLOR_BGR2RGB))
    pixelMap = picture.load()

    avgColor = 0
    pixelCount = 0

    #find average color
    w, h = picture.size
    for i in range(w):
        for j in range(h):
            b, g, r = picture.getpixel((i, j))
            avgColor = (b + g + r)/3 + avgColor
            pixelCount = pixelCount + 1

    avgColor = avgColor / pixelCount
            
    #convert to pure black and white
    w, h = picture.size
    for i in range(w):
        for j in range(h):
            b, g, r = picture.getpixel((i, j))
            if (r + b + g)/3 < avgColor - 10:
                pixelMap[i, j] = (0, 0, 0)
            else:
                pixelMap[i, j] = (255, 255, 255)

    #convert pil back to cv2
    picture = np.array(picture)
    picture = picture[:, :, ::-1].copy()

    return picture


#get average width and height of each letter box (used for dummy crabons)
def avgWH(letterBoxes):

    WTotal = 0
    HTotal = 0
    for i in range(len(letterBoxes)):
        X, Y, W, H, L = letterBoxes[i]
        WTotal = WTotal + W
        HTotal = HTotal + H

    WTotal = WTotal/len(letterBoxes)
    HTotal = HTotal/len(letterBoxes)

    return WTotal, HTotal


#get average length of the lines
def avgLineLength(lines):

    totalDistance = 0
    for i in range(len(lines)):
        X1, Y1, X2, Y2 = lines[i]
        distance = math.sqrt((X1 - X2)**2 + (Y1 - Y2)**2)
        totalDistance = totalDistance + distance

    totalDistance = totalDistance / len(lines)
    return totalDistance        


#map each point of an edge to a letter box
def mapEdges(letterBoxes, lines):

    #the lists are used for the bounding box, not the actual box containing the letter
    #the bounding box is larger than the letter box
    boundXlist = []
    boundYlist = []
    boundWlist = []
    boundHlist = []
    boundLlist = []
    boundExpand = 2     #multiplier for width and height

    #holds dummy carbons in addition to other letter boxes
    #dummy carbon label is lowercase 'c'
    letterBoxesWithDummies = letterBoxes.copy() 

    #expand the bounds of the letterBoxes
    for i in range(len(letterBoxes)):
        boundX, boundY, boundW, boundH, boundL = letterBoxes[i]
        boundXlist.append(boundX - 0.5 * (boundExpand - 1) * boundW)
        boundYlist.append(boundY - 0.5 * (boundExpand - 1) * boundH)
        boundWlist.append(boundW * boundExpand)
        boundHlist.append(boundH * boundExpand)
        boundLlist.append(boundL)
        letterBoxesWithDummies[i] = boundXlist[i], boundYlist[i], boundWlist[i], boundHlist[i], boundLlist[i]

    #get average box size for dummy carbons
    if len(letterBoxes) > 0:
        avgW, avgH = avgWH(letterBoxes)
    else:
        avgW, avgH = avgLineLength(lines)

    #create dummy carbons (carbons represented as two lines touching, not as a visible 'C'
    for i in range(len(lines)):
        X1, Y1, X2, Y2 = lines[i]
        notMatched1 = True
        notMatched2 = True
        #iterate through each expanded letter box
        for j in range(len(boundLlist)):
            #test if point 1 is inside bounding box
            if (X1 > boundXlist[j]) and (X1 < boundXlist[j] + boundWlist[j]) and (Y1 > boundYlist[j]) and (Y1 < boundYlist[j] + boundHlist[j]):
                notMatched1 = False
            #test if point 2 is inside bounding box
            elif (X2 > boundXlist[j]) and (X2 < boundXlist[j] + boundWlist[j]) and (Y2 > boundYlist[j]) and (Y2 < boundYlist[j] + boundHlist[j]):
                notMatched2 = False

        #if point 1 or point 2 don't have a matched element, create a dummy carbon and the bounds for that dummy carbon
        #don't expand  the bounds, the dummies are big enough
        if notMatched1:
            letterBoxesWithDummies.append((X1 - avgW/2, Y1 - avgH/2, avgW, avgH, 'c'))
            boundXlist.append(X1 - avgW/2)
            boundYlist.append(Y1 - avgH/2)
            boundWlist.append(avgW)
            boundHlist.append(avgH)
            boundLlist.append('c')
        elif notMatched2:
            letterBoxesWithDummies.append((X2 - avgW/2, Y2 - avgH/2, avgW, avgH, 'c'))
            boundXlist.append(X2 - avgW/2)
            boundYlist.append(Y2 - avgH/2)
            boundWlist.append(avgW)
            boundHlist.append(avgH)
            boundLlist.append('c')

    #initialize a 2d array full of 0's
    edgeList = []
    row = []
    for i in range(len(lines)):
        for j in range(len(letterBoxesWithDummies)):
            row.append('+')
        edgeList.append(row)
        row = [] 
        

    #iterate through each line
    for i in range(len(lines)):
        X1, Y1, X2, Y2 = lines[i]
        #iterate through each expanded letter box
        for j in range(len(boundLlist)):
            #test if point 1 is inside bounding box
            if (X1 > boundXlist[j]) and (X1 < boundXlist[j] + boundWlist[j]) and (Y1 > boundYlist[j]) and (Y1 < boundYlist[j] + boundHlist[j]):
                edgeList[i][j] = boundLlist[j]
            #test if point 2 is inside bounding box
            elif (X2 > boundXlist[j]) and (X2 < boundXlist[j] + boundWlist[j]) and (Y2 > boundYlist[j]) and (Y2 < boundYlist[j] + boundHlist[j]):
                edgeList[i][j] = boundLlist[j]

    return letterBoxesWithDummies, edgeList


def condenseLines(linesArg, avgSquare):

    #convert lines argument into a better array
    allLines = []
    for i in range(len(linesArg)):
        allLines.append(linesArg[i][0])

    lines = []
    #get rid of short lines, anything shorter than half the square width is gotten rid of
    for i in range(len(allLines)):
        X1, Y1, X2, Y2 = allLines[i]
        distance = math.sqrt((X1 - X2)**2 + (Y1 - Y2)**2)
        if distance > avgSquare / 2:
            lines.append(allLines[i])

    condensedLines = []
    isPair = True
    while isPair:
        isPair = False
        distances = []
        #first line data
        for i in range(len(lines)):
            #end loop early when it should have ended anyways (python issue or something, fixes bug)
            if i >= len(lines):
                break

            #get angle of first line
            X1, Y1, X2, Y2 = lines[i]
            if X1 - X2 == 0:
                angle1 = math.pi / 2
            else:
                angle1 = math.atan((Y1 - Y2) / (X1 - X2)) 

            #find angle flipped 90 degrees (important for angles close to 90 degrees or -90 degrees)
            if Y1 - Y2 == 0:
                sideAngle1 = math.pi / 2
            else:
                sideAngle1 = math.atan((X1 - X2) / (Y1 - Y2))
            
            #second line data
            for j in range(len(lines)):

                #get angle of second line
                XX1, YY1, XX2, YY2 = lines[j]
                if XX1 - XX2 == 0:
                    angle2 = math.pi / 2
                else:
                    angle2 = math.atan((YY1 - YY2) / (XX1 - XX2))

                #find angle flipped 90 degrees
                if YY1 - YY2 == 0:
                    sideAngle2 = math.pi / 2
                else:
                    sideAngle2 = math.atan((XX1 - XX2) / (YY1 - YY2))

                #if parallel and different lines, record distance
                if ((abs(angle1 - angle2) < math.pi / 12) or (abs(sideAngle1 - sideAngle2) < math.pi / 12)) and i != j:
                    isPair = True
                    #get midpoints of each line to calculate distance
                    midX = (X1 + X2)/2
                    midY = (Y1 + Y2)/2
                    midXX = (XX1 + XX2)/2
                    midYY = (YY1 + YY2)/2
                    #add distances between midpoints of lines to distances
                    distances.append((math.sqrt((midX - midXX)**2 + (midY - midYY)**2), i, j))

        if isPair:
            #find smallest distance
            smallestDistance, ii, jj = distances[0]
            for i in range(len(distances)):
                if distances[i][0] < smallestDistance:
                    smallestDistance, ii, jj = distances[i]

            #find the largest of the two lines in the pair
            X1, Y1, X2, Y2 = lines[ii]
            length = math.sqrt((X1 - X2)**2 + (Y1 - Y2)**2)
            XX1, YY1, XX2, YY2 = lines[jj]
            llength = math.sqrt((XX1 - XX2)**2 + (YY1 - YY2)**2)
            if length < llength:
                X1, Y1, X2, Y2 = XX1, YY1, XX2, YY2

            #add line to condensed lines list, and remove the original lines from the lines list
            condensedLines.append((X1, Y1, X2, Y2))
            lines.pop(jj)
            lines.pop(ii)
   
    return condensedLines



'''
for i in range(len(letterBoxes)):
    print(letterBoxes[i][4], ' ', sep='', end='')


for i in range(len(edgeMap)):
    print()
    for j in range(len(edgeMap[i])):
        print(edgeMap[i][j], ' ', sep='', end='')
'''










                        

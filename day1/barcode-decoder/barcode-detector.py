import sys
import numpy as np
import copy
import cv2
import math
from collections import defaultdict
from matplotlib import pyplot as plt
from barcodeReader import read_and_print_barcode

path = './input.png'
if len(sys.argv) > 1:
    path = sys.argv[1]

img_path = path
original = cv2.imread(img_path)
image = original.copy()
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

image = cv2.resize(image,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_CUBIC)
original = cv2.resize(original,None,fx=0.7, fy=0.7, interpolation = cv2.INTER_CUBIC)


# applying a sobel filter for edge enhancement and getting the gradients
gradX = cv2.Sobel(image, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
gradY = cv2.Sobel(image, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)

#plt.imshow(gradX, cmap='gray')
#plt.imshow(gradY, cmap='gray')

gradient = cv2.sqrt(cv2.add((gradX * gradX), (gradY * gradY)))
gradient = cv2.convertScaleAbs(gradient) # Converts the output to an 8-bit representation

# blurred = # Blur the gradient image using cv2.blur() with a 3*3 kernel
gradient_blur = cv2.blur(gradient, (3, 3))

#plt.imshow(gradient_blur, cmap='gray')

threshold  = 225
_, gradient_thresh = cv2.threshold(
    gradient_blur, thresh=threshold,
    maxval=255, type=cv2.THRESH_BINARY 
)

thresh = copy.deepcopy(gradient_thresh)

kernel = cv2.getStructuringElement(shape=cv2.MORPH_RECT, ksize=(21, 7)) # Define a rectangular kernal with W = 21 and H = 7

# Perform the morphological closing operation on "thresh" using the above kernel
closed = cv2.morphologyEx(
    thresh, op=cv2.MORPH_CLOSE,
    kernel=kernel
) 

closed = cv2.dilate(closed, None, iterations = 7) # Performs dilation operation on the closed image

# these cnts are tuples of numpy array, each numpy array contains all the white pixels of one detected contour
cnts,hierarchy = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
c = sorted(cnts, key = cv2.contourArea, reverse = True)[0] # Finds the region with maximum area

rect = cv2.minAreaRect(c) # Fits a minimum area rectangle over the region with maximum area, hence creating a rectangular bounding box around the barcode
box = np.intp(cv2.boxPoints(rect))

img = copy.deepcopy(original)
#cv2.drawContours(img, [box], -1, (0, 0, 255), thickness=1)

# This function crops the bounding box
def getSubImage(rect, src):
    center, size, theta = rect 
    size = [size[1],size[0]]
    center, size = tuple(map(int, center)), tuple(map(int, size))
    M = cv2.getRotationMatrix2D( center, theta-90, 1)
    print(src.shape)
    dst = cv2.warpAffine(src, M, [src.shape[1],src.shape[0]])
    out = cv2.getRectSubPix(dst, size, center)
    return out

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = getSubImage(rect, img)

#print(f'barcode-detector: img.shape: {img.shape}')
#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#plt.imshow(img, cmap='gray')

#plt.show()

read_and_print_barcode(img)

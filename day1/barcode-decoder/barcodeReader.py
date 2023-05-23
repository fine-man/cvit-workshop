import sys
import numpy as np
import copy
import cv2
import math
from collections import defaultdict
from matplotlib import pyplot as plt

encoding_pattern ={
        "111111":0,
        "110100":1,
        "110010":2,
        "110001":3,
        "101100":4,
        "100110":5,
        "100011":6,
        "101010":7,
        "101001":8,
        "100101":9
}

left=[
    {
        "0100111":0,
        "0110011":1,
        "0011011":2,
        "0100001":3,
        "0011101":4,
        "0111001":5,
        "0000101":6,
        "0010001":7,
        "0001001":8,
        "0010111":9   
    },
    {
        "0001101":0,
        "0011001":1,
        "0010011":2,
        "0111101":3,
        "0100011":4,
        "0110001":5,
        "0101111":6,
        "0111011":7,
        "0110111":8,
        "0001011":9   
    }
]

right = {
        "1110010":0,
        "1100110":1,
        "1101100":2,
        "1000010":3,
        "1011100":4,
        "1001110":5,
        "1010000":6,
        "1000100":7,
        "1001000":8,
        "1110100":9 
}
# Write a function that takes in a 3-channel RGB image as input, converts it 
# into a 1-channel grayscale image, and returns the converted grayscale image.
# Note that to convert an RGB image to grayscale, we take the weighted average
# of the RGB components as Gray = 0.2989 * RED + 0.5870 * GREEN + 0.1140 * BLUE
def rgb2gray(rgb):
  # WRITE YOUR CODE HERE
  img_gray = 0.2989 * rgb[:, :, 0] + 0.5870 * rgb[:, :, 1] + 0.1140 * rgb[:, :, 2]
  return img_gray

# Write a function that takes a 1-channel grayscale image, and the thresholding value 
# as inputs, and performs binary thresholding on the input image with the given threshold.
# i.e. if threshold is thrs, then all pixels with intensity < thrs should become 0, and 
# all pixels with intensity >= thrs should become 255
def thresholding(img, thrs):
  # WRITE YOUR CODE HERE
    _, thresh = cv2.threshold(
        img, thresh=thrs,
        maxval=255, type=cv2.THRESH_BINARY
    )

    return thresh

# This function takes an RGB image as input, converts it into grayscale image, performs 
# binary thresholding on the grayscale image, and then finally returns the image.
def binarise(pic, thrs):
  img = rgb2gray(pic) # Converts the image from RGB to Grayscale
  threshimg = thresholding(img, thrs) # Performs binary thresholding on the input image
  return threshimg

def primitive_crop(row):
    """
    crops the row to the first and last occurance of black pixel (0 pixel value)
    """
    indices = np.where(row == 0)[0]
    if indices.shape[0] == 0:
      return None
    return row[indices[0]:indices[-1]+1]

def convert_binary(bars,nlb):
    """
    converts a barcode image row containing 0 or 255
    to a binary string.

    bars: cropped row of binary image
    nlb: Number of pixels per binary digit

    returns a string containing 0 and 1s
    """
    binstring = ''
    d = 1
    cnt = 0
    np.append(bars,[-1])
    for i in bars:
      if i == (255 - d*255):
        cnt = cnt + 1
      else:
        if d == 1:
          d = 0
          binstring = binstring + '1'*math.ceil(cnt/nlb)
        else:
          d = 1
          binstring = binstring + '0'*math.floor(cnt/nlb)
        cnt = 1
    return binstring

def find_num_bars(cropped_row):
    """
    Finds the number of pixels associated with one bar
    """
    
    num = 0
    for i in cropped_row:
        if i == 255:
            break
        else:
            num += 1
    return num

def find_encoding(bs_list):
    """
    returns the encoding (string) to be used to decode the list of binary strings

    bs_list : list of binary strings where each binary string
    correspond to a decimal digit (using some encoding)
    """
    par_str = ""
    for number in range(6):
        parity = 0
        for i in bs_list[number]:
            parity ^= int(i)
        par_str += str(parity)
    return par_str

def get_digits(binary_string,rep_length):
    """
    returns the list of non-decoded binary string versions of decimal digits

    binary_string : binary string containing 0s and 1s
    rep_length : number of binary digits that correspond to one decimal digit after decoding
    """
    number_strings = []
    start_pos = 3
    end_pos = len(binary_string) - 3
    i = start_pos
    while(i < end_pos):
        if i == start_pos + rep_length*6:
            i+=5
            continue
        number_strings.append(str(binary_string[i:i+rep_length]))
        i += rep_length
    return number_strings

def decode(encoding_pattern_number,bs_list):
    """
    decodes a list of barcode binary string using barcode-EAN13 algorithm

    encoding_patter_number: binary string which is to be used to find encoding_number
    bs_list: list of binary strings where each string is encoding of some decimal digit

    returns a string containing the decoded decimal digits
    """

    info = ""
    info += str(encoding_pattern[encoding_pattern_number]) + '-'
    for i in range(6):
        info += str(left[int(encoding_pattern_number[i])][bs_list[i]])
    info += '-'
    for i in range(6,12):
        info += str(right[bs_list[i]])
    return info

def pre_process_image(image):
    """
    resizes the image and turns it into a binary image
    """
    print(image.shape)
    img = copy.deepcopy(image)
    img = img.astype('uint8')
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    histr = cv2.calcHist([img],[0],None,[256],[0,256])
    #plt.plot(histr)
    #plt.show()

    image_cropped = copy.deepcopy(img)
    image_cropped = cv2.resize(image_cropped, (219, 150))
    bimg = binarise(image_cropped, 100)
    return bimg

def read_and_print_barcode(img):
    """
    reads the barcode from a image containing only barcode
    and then prints the decoded barcoded
    """
    bimg = pre_process_image(img)
    #print(f'read_and_print: bimg.shape={bimg.shape}')

    ctr = defaultdict(int)
    for row in bimg:
      cropped_row = primitive_crop(row)
      if cropped_row is None:
        continue
      try:
        nlb = find_num_bars(cropped_row)
        binary_string = convert_binary(cropped_row,nlb)
        rep_length = 7
        num_numbers = 13
        bs_list = get_digits(binary_string,rep_length)
        encoding_pattern_number = find_encoding(bs_list)
        information = decode(encoding_pattern_number,bs_list)
        ctr[information] +=1
      except:
        continue

    if len(list(ctr.keys())):
      print('Scanned Barcode:',list(ctr.keys())[0])
    else:
      print('Barcode Scanning Failed!!!')

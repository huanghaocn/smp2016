__author__ = 'qibai'
from PIL import Image
# from pylab import *
import numpy as np
import os
import cv2

im = np.array(Image.open("/home/qibai/Documents/smpData/valid_images/1047273002"))
print im.shape
def getCosine(a, b):
    ab_sum = np.dot(a, b.T)
    a_sum_square = np.dot(a, a.T)
    b_sum_square = np.dot(b, b.T)
    if a_sum_square == 0 or b_sum_square == 0:
        return 0
    return float(ab_sum) / (np.sqrt(a_sum_square) * np.sqrt(b_sum_square))


male = "/home/qibai/Documents/smpData/valid_images/1047273002"
maleIm = np.array(Image.open(male)).reshape((1, 180 * 180))
female = "/home/qibai/Documents/smpData/images/2336510900"
femaleIm = np.array(Image.open(female)).reshape((1, 180 * 180))
dirname = "/home/qibai/Documents/smpData/valid_images/"
images = {}
labels = {}
# lines = open("/home/qibai/Documents/smpData/communityDetect/label_maps.csv")
# for line in lines:
#     items = line.strip().split(",")
#     labels[items[0]] = items[2]
for parent, dirnames, filenames in os.walk(dirname):
    for filename in filenames:
        # if filename not in labels:
        #     print ("can't find user :" + filename)
        #     continue
        images[filename] = os.path.join(parent, filename)

for image in images:
    im = np.array(Image.open(images.get(image)))
    if len(im.shape) == 2:
        if getCosine(maleIm, im.reshape((1, 180 * 180)))==1:
            print image+"male"
        if getCosine(femaleIm, im.reshape((1, 180 * 180)))==1:
            print image+"female"

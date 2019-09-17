import cardDetect
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2 as cv
import glob

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-bg", "--bgthresh", help = "threshold value for background")
ap.add_argument("-i", "--image", help = "'One' or 'Two'")
args = vars(ap.parse_args())

# Image path setup
img = cv.imread(args["image"])
BKG_THRESH = int(args["bgthresh"])
images = glob.glob('./Basic/*.png')

# Loop through
pos = 1
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    # Process Image
    thresh = cardDetect.thresh(gray, BKG_THRESH)
    
    bound = cardDetect.bound(img, thresh)

# Plot
# plt.subplot(231),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(232),plt.imshow(thresh,cmap = 'gray')
# plt.title('Threshold'), plt.xticks([]), plt.yticks([])
# plt.subplot(233),plt.imshow(bound,cmap = 'gray')
# plt.title('Boundary Box'), plt.xticks([]), plt.yticks([])
# plt.show()
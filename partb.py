import cardDetect
from calibrate import calibrateCamera as calibrate
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2 as cv
import glob

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imageset", help = "'Basic', 'Skillful' or 'Advanced'")
args = vars(ap.parse_args())

# Imagesetup
imageset = args["imageset"]

if imageset == "Basic":
    images = glob.glob('./Basic/*.png')
    calibset = './Calibration - Two/'
elif imageset == "Skillful":
    images = glob.glob('./Skillful/*.png')
    calibset = './Calibration - One/'
elif imageset == "Advanced":
    images = glob.glob('./Advanced - Set 2/*.png')
    calibset = './Calibration - Three/'
else:
    print("pick an actual imageset pls")

ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints = calibrate(calibset)

# Parameters
BKG_THRESH = 40
canny_thresh = 5
dilation = 10

# Loop through
pos = 0
for fname in images:

    # Select image
    img = cv.imread(fname)
    w, h = img.shape[0], img.shape[1]

    # # Undistort
    # newcameramtx, roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    # img = cv.undistort(img, mtx, dist, None, newcameramtx)

    # Colour setup
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    # Process Image
    thresh, edges, dilated = cardDetect.preprocess(gray, BKG_THRESH, canny_thresh, dilation)
    segmented = thresh - edges
    bound, cards = cardDetect.bound(img, segmented)
    
    # Save and print results
    print(f'Image {pos}:')
    for i in range(len(cards)):
        minDist, pt1, pt2 = cardDetect.minDistance(cards[i].contour, cards[i-1].contour)
        cv.line(bound, pt1, pt2, (0, 0, 255), 2)
        print(f'Card {cards[i].id+1}: Pos = {cards[i].center}')
        print(f'Minimum distance from card {cards[i].id+1} to card {cards[i-1].id+1}: {minDist}')

    # Prep results for plotting
    bound = cv.cvtColor(bound, cv.COLOR_BGR2RGB)
    bound = cv.resize(bound, (0, 0), None, .5, .5)
    edges = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
    edges = cv.resize(edges, (0, 0), None, .5, .5)

    # Plot
    final_frame = cv.hconcat([bound, edges])
    cv.imshow("yeet", final_frame)
    cv.waitKey(1000)

    pos += 1

# Plot
# plt.subplot(231),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(232),plt.imshow(thresh,cmap = 'gray')
# plt.title('Threshold'), plt.xticks([]), plt.yticks([])
# plt.subplot(233),plt.imshow(edges,cmap = 'gray')
# plt.title('Edges'), plt.xticks([]), plt.yticks([])
# plt.subplot(234),plt.imshow(dilated,cmap = 'gray')
# plt.title('Dilated'), plt.xticks([]), plt.yticks([])
# plt.subplot(235),plt.imshow(segmented,cmap = 'gray')
# plt.title('Segmented'), plt.xticks([]), plt.yticks([])
# plt.subplot(236),plt.imshow(bound,cmap = 'gray')
# plt.title('Boundary Box'), plt.xticks([]), plt.yticks([])
# plt.show()
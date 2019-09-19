import cardDetect
from calibrate import calibrateCamera as calibrate
import numpy as np
import matplotlib.pyplot as plt
import argparse
import cv2 as cv
import glob

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imageset", help = "'Basic', 'Skillful' or 'Advanced'")
ap.add_argument("-d", "--mindist", help = "Prints the minimum distance between cards")
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

# ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints = calibrate(calibset)

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
    # segmented = thresh - edges
    bound, cards = cardDetect.bound(img, thresh)
    
    # Save and print results
    print(f'Image {pos}:')
    for i in range(len(cards)):
        theta = cardDetect.get_theta(cards[i])
        centerx = cards[i].center[0] - (w/2)
        centery = -(cards[i].center[1] - (h/2))
        print(f'Card {cards[i].id+1}: Pos = ({centerx}, {centery}) Theta = {theta}')
        # cv.line(bound, cards[i].center, , (0, 0, 255), 2)
        if str2bool(args["mindist"]):
            minDist, pt1, pt2 = cardDetect.minDistance(cards[i].contour, cards[i-1].contour)
            print(f'Minimum distance from card {cards[i].id+1} to card {cards[i-1].id+1}: {minDist}')
            cv.line(bound, pt1, pt2, (0, 0, 255), 2)

    # Prep results for plotting
    bound = cv.cvtColor(bound, cv.COLOR_BGR2RGB)
    bound = cv.resize(bound, (0, 0), None, .5, .5)
    edges = cv.cvtColor(edges, cv.COLOR_GRAY2BGR)
    edges = cv.resize(edges, (0, 0), None, .5, .5)

    # Plot
    final_frame = cv.hconcat([bound, edges])
    cv.imshow("yeet", final_frame)
    cv.waitKey(1000)
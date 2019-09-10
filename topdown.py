import mycv.transform as tform
from mycv.calibrate import calibrateCamera as calibrate
import numpy as np
import argparse
import cv2 as cv
import glob

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imageset", help = "'One' or 'Two'")
args = vars(ap.parse_args())
imageset = f'./Calibration - {args["imageset"]}/'
print(imageset)

# Calibrate Camera
ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints = calibrate(imageset) # Calibrate camera

# Image path setup
warpImg = glob.glob(f'{imageset}/*.png')

# Create files
pos = 1
for fname in warpImg:
    img = cv.imread(fname)
    w, h = img.shape[0], img.shape[1]

    # Undistort
    newcameramtx, roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    img = cv.undistort(img, mtx, dist, None, newcameramtx)

    # Transform
    src, dst = tform.get_points(img, (8,6))
    warped, M = tform.warp(img, src, dst)

    cv.imwrite(f'./Top Down - {args["imageset"]}/result{pos}.png', warped)
    pos += 1
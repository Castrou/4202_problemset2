import transform as tform
from calibrate import calibrateCamera as calibrate
import numpy as np
import argparse
import cv2 as cv
import glob

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imageset", help = "'One' or 'Two'")
ap.add_argument("-d", "--display", help = "1 or 0")
args = vars(ap.parse_args())
imageset = f'./Calibration - {args["imageset"]}/'
disp = int(args["display"])

# Calibrate Camera
pattern_size = (8,6)
ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints = calibrate(imageset, pattern_size) # Calibrate camera
print("focal length (x) = "+str(mtx[0][0]))
print("focal length (y) = "+str(mtx[1][1]))
print("x offset from center = " + str(mtx[0][2]))
print("y offset from center = " + str(mtx[1][2]))
print("skew = " + str(mtx[0][1]))

# Image path setup
warpImg = glob.glob(f'{imageset}/*.png')

# Create files
for fname in warpImg:
    img = cv.imread(fname)
    w, h = img.shape[0], img.shape[1]

    # Undistort
    newcameramtx, roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    img = cv.undistort(img, mtx, dist, None, newcameramtx)

    # Transform
    try:
        src, dst = tform.get_points(img, pattern_size)
        warped, M = tform.warp(img, src, dst, disp)
        cv.imwrite(f'./Top Down - {args["imageset"]}/warped_{fname[len(imageset):]}', warped)
        print(f"warped_{fname[len(imageset):]}")
    except cv.error:
        print(f"Unable to find points for {fname[len(imageset):]}")

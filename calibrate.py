import cv2 as cv 
import numpy as np 
import glob

def calibrateCamera(dataPATH, disp=0):
    # termination criteria
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((6*8,3), np.float32)
    objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

    # Init object (3D in real world) and image (2D in image plane) points
    objpoints = []
    imgpoints = []

    calibImg = glob.glob(f'{dataPATH}*.png')

    for fname in calibImg:
        img = cv.imread(fname)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Find corners
        ret, corners = cv.findChessboardCorners(img, (8,6), None)

        # If found, add refined object and image points
        if ret == True:
            objpoints.append(objp)
            corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners)

            if disp:
                # Draw and display the corners
                cv.drawChessboardCorners(img, (8,6), corners2, ret)
                cv.imshow('img', img)
                cv.waitKey(500)

    cv.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return ret, mtx, dist, rvecs, tvecs, objpoints, imgpoints


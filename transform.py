import numpy as np
import matplotlib.pyplot as plt
import cv2
 
def get_points(img, region, sqsize=25):
	ret, corners = cv2.findChessboardCorners(img, region, None)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, src = cv2.find4QuadCornerSubpix(gray, corners, region)
	src = np.array([src[0][0],src[region[0]-1][0],src[-region[0]][0],src[-1][0]])
	# cv2.drawChessboardCorners(img, (8,6), src, ret)
	# cv2.imshow('img', img)
	# cv2.waitKey(500)
	pt1 = src[0]
	pt2 = (src[0][0]+sqsize*region[0],src[0][1])
	pt3 = (src[0][0],src[0][1]+sqsize*region[1])
	pt4 = (src[0][0]+sqsize*region[0],src[0][1]+sqsize*region[1])
	dst = np.float32([pt1, pt2, pt3, pt4])
	return src, dst

def warp(img, src, dst, testing=False):
    h, w = img.shape[:2]
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse
    M = cv2.getPerspectiveTransform(src, dst)
    # use cv2.warpPerspective() to warp your image to a top-down view
    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)

    if testing:
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
        f.subplots_adjust(hspace=.2, wspace=.05)
        ax1.imshow(img)
        x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
        y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]
        ax1.plot(x, y, color='red', alpha=0.4, linewidth=3, solid_capstyle='round', zorder=2)
        ax1.set_ylim([h, 0])
        ax1.set_xlim([0, w])
        ax1.set_title('Original Image', fontsize=30)
        ax2.imshow(cv2.flip(warped, 1))
        ax2.set_title('Warped Image', fontsize=30)
        plt.show()
    
    return warped, M
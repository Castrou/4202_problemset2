import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

def edge(img):
    dilate_kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,5))
    open_kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(15,15))

    # Parameters
    canny_threshold = 50
    sigma_x = 2
    blur_intensity = 7

    # Start Processing Images
    blurred = cv.GaussianBlur(img, (blur_intensity, blur_intensity), sigma_x)
    edges = cv.Canny(blurred, canny_threshold, 0.4*canny_threshold)
    dilated = cv.dilate(edges, dilate_kernel, iterations = 1)
    filled = cv.imgfill(dilated, 100)
    opened = cv.morphologyEx(filled, cv.MORPH_OPEN, open_kernel)

    # Plotd
    plt.subplot(231),plt.imshow(img,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(232),plt.imshow(blurred,cmap = 'gray')
    plt.title('Guassian Blur'), plt.xticks([]), plt.yticks([])
    plt.subplot(233),plt.imshow(edges,cmap = 'gray')
    plt.title('Edges'), plt.xticks([]), plt.yticks([])
    plt.subplot(234),plt.imshow(dilated,cmap = 'gray')
    plt.title('Dilation'), plt.xticks([]), plt.yticks([])
    # plt.subplot(235),plt.imshow(opened,cmap = 'gray')
    # plt.title('Opening'), plt.xticks([]), plt.yticks([])
    plt.show()
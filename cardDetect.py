import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

CARD_MAX_AREA = 130000
CARD_MIN_AREA = 12000

class Card:
    """ Information about card """
    def __init__(self):
        self.contour = []
        self.width, self.height = 0,0
        self.corner_pts = []
        self.center = 0
        self.id = 0

def minDistance(contour, contourOther):
    distanceMin = 99999999
    pos = 0
    for point1 in contour:
        for point2 in contourOther:
            distance = 0
            xA, yA = point1[0][0], point1[0][1]
            xB, yB = point2[0][0], point2[0][1]
            distance = ((xB-xA)**2+(yB-yA)**2)**(1/2) # distance formula
            if (distance < distanceMin):
                distanceMin = distance
                xAmin, yAmin, xBmin, yBmin  = xA, yA, xB, yB
        pos += 1
    return distanceMin, (xAmin, yAmin), (xBmin, yBmin)

def get_theta(qCard):
    # print(qCard.corner_pts[0][0])
    hyp = 9999999
    # [xB, yB], [xA, yA] = qCard.corner_pts[0][0], qCard.corner_pts[1][0]
    xA, yA = qCard.center
    for point in qCard.contour:
        xB, yB = point[0][0], point[0][1]
        distance = ((xB-xA)**2+(yB-yA)**2)**(1/2)
        if (distance < hyp):
            hyp = distance
            xlineB, xlineA = xB, xA
    xline = abs(xlineB-xlineA)
    theta = np.arccos(xline/hyp)
    theta = theta*180 / np.pi
    return theta

def preprocess(img, BKG_THRESH=40, canny_thresh=50, dilation=5):

    # Start Processing Images
    blur = cv.GaussianBlur(img,(5,5),0)

    img_w, img_h = np.shape(img)[:2]
    bkg_level = img[int(img_h/100)][int(img_w/2)]
    thresh_level = bkg_level + BKG_THRESH
    dilate_kernel = cv.getStructuringElement(cv.MORPH_RECT,(dilation,dilation))

    retval, thresh = cv.threshold(blur,thresh_level,255,cv.THRESH_BINARY)
    edges = cv.Canny(thresh, canny_thresh, 0.4*canny_thresh)
    dilated = cv.dilate(edges, dilate_kernel, iterations = 1)
    
    return thresh, edges, dilated

def find_cards(thresh_img):

    cnts,hier = cv.findContours(thresh_img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    index_sort = sorted(range(len(cnts)), key=lambda i : cv.contourArea(cnts[i]),reverse=True)

    # If there are no contours, do nothing
    if len(cnts) == 0:
        return [], []

    # Otherwise, initialize empty sorted contour and hierarchy lists
    cnts_sort = []
    hier_sort = []
    cnt_is_card = np.zeros(len(cnts),dtype=int)

    # Fill empty lists with sorted contour and sorted hierarchy. Now,
    # the indices of the contour list still correspond with those of
    # the hierarchy list. The hierarchy array can be used to check if
    # the contours have parents or not.
    for i in index_sort:
        cnts_sort.append(cnts[i])
        hier_sort.append(hier[0][i])

    # Determine which of the contours are cards by applying the
    # following criteria: 1) Smaller area than the maximum card size,
    # 2), bigger area than the minimum card size, 3) have no parents,
    # and 4) have four corners

    for i in range(len(cnts_sort)):
        size = cv.contourArea(cnts_sort[i])
        peri = cv.arcLength(cnts_sort[i],True)
        approx = cv.approxPolyDP(cnts_sort[i],0.01*peri,True)
        
        if ((size < CARD_MAX_AREA) and (size > CARD_MIN_AREA)
            and (hier_sort[i][3] == -1) and (len(approx) == 4)):
            cnt_is_card[i] = 1

    return cnts_sort, cnt_is_card

def preprocess_card(contour, image):
    """Uses contour to find information about the card."""

    # Initialize new Card object
    qCard = Card()

    qCard.contour = contour

    # Find perimeter of card and use it to approximate corner points
    peri = cv.arcLength(contour,True)
    approx = cv.approxPolyDP(contour,0.01*peri,True)
    pts = np.float32(approx)
    qCard.corner_pts = pts

    # Find width and height of card's bounding rectangle
    x,y,w,h = cv.boundingRect(contour)
    qCard.width, qCard.height = w, h

    # Find center point of card by taking x and y average of the four corners.
    average = np.sum(pts, axis=0)/len(pts)
    cent_x = int(average[0][0])
    cent_y = int(average[0][1])
    qCard.center = [cent_x, cent_y]

    return qCard

def bound(img, thresh_img):

    bound = img
    # Find and sort the contours of all cards in the image (query cards)
    cnts_sort, cnt_is_card = find_cards(thresh_img)

    # If there are no contours, do nothing
    if len(cnts_sort) != 0:

        # Initialize a new "cards" list to assign the card objects.
        # k indexes the newly made array of cards.
        cards = []
        k = 0

        # For each contour detected:
        for i in range(len(cnts_sort)):
            if (cnt_is_card[i] == 1):

                # Create a card object from the contour and append it to the list of cards.
                cards.append(preprocess_card(cnts_sort[i],bound))
	    
        # Draw card contours on image (have to do contours all at once or
        # they do not show up properly for some reason)
        if (len(cards) != 0):
            temp_cnts = []
            for i in range(len(cards)):
                temp_cnts.append(cards[i].contour)
                cards[i].id = i
                # for j in range(4):
                #     pt1 = tuple(cards[i].corner_pts[j-1][0])
                #     pt2 = tuple(cards[i].corner_pts[j][0])
                #     cv.line(bound, pt1, pt2, (255, 0, 0), 2)
            cv.drawContours(bound,temp_cnts, -1, (255,0,0), 2)
        
    return bound, cards
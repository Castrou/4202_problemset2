from edge import edge
import numpy as np
import argparse
import cv2 as cv
import glob

# Argument parsing
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "'One' or 'Two'")
args = vars(ap.parse_args())

# Image path setup
img = cv.imread(args["image"], 0)
edge(img)

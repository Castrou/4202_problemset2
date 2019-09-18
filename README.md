# 4202 Problem Set2
## Installation:
_pip install opencv-python_  
_pip install matplotlib_  
_pip install numpy_  

# How to use:
## Part A:
Run with the following command:  
_python parta.py --imageset {imageset}_

Replace {imageset} with either "One", "Two" or "Three", depending on the image set you'd like to you (ie. "Calibration - One" or "Calibration - Two")

The intrinsic values resulting from calibration will be printed, and a topdown perspective of the imageset will be created in either "Top Down - One" or "Top Down - Two" depending on the imageset chosen

## Part B:
Run with the following command: 
_python partb.py --imageset {imageset} --mindist {bool}_

Replace {imageset} with either "Basic", "Skillful" or "Advanced"  
Replace {bool} with either True or False  
This will print the boundaries around cards and the detected edges for each image in the set  
Setting mindist to True will print the minimum distances between them (this is much slower)

NOTE: Currently, only "Basic" has full functionality
# 4202 Problem Set2
## Installation:
_pip install opencv-python_  
_pip install matplotlib_  
_pip install numpy_  
_git clone https://github.com/Castrou/4202_problemset2_

# How to use:
## Part A:
Run with the following command:  
_python parta.py --imageset {imageset} --showcalib {sc} --showwarp {sw}_

Replace {imageset} with either "One", "Two" or "Three", depending on the image set you'd like to you (ie. "Calibration - One", "Calibration - Two", "Calibration - Three")
Replace {sc} with either 1 to display the calibrated chessboard corners.
Replace {sw} with either 1 to display the warped image compared to original.

The intrinsic values resulting from calibration will be printed, and a topdown perspective of the imageset will be created in either "Top Down - One", "Top Down - Two" or "Top Down - Three" depending on the imageset chosen

## Part B:
Run with the following command: 
_python partb.py --imageset {imageset} --mindist {bool}_

Replace {imageset} with either "Basic", "Skillful" or "Advanced"  
Replace {bool} with either True or False  
This will print the boundaries around cards and the detected edges for each image in the set  
Setting mindist to True will print the minimum distances between them (this is much slower)

NOTE: Currently, only "Basic" has full functionality
NOTE: If you need to clear results to check if it writes to a file DO NOT delete the folder. Delete the files within the folder instead.
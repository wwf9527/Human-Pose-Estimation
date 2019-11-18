import numpy as np
import cv2 
import sys
import os
from sys import platform
import argparse

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    # Windows Import
    if platform == "win32":
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append(dir_path + '/../../python/openpose/Release');
        os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
        import pyopenpose as op
    else:
        # Change these variables to point to the correct folder (Release/x64 etc.)
        sys.path.append('../../python');
        # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
        # sys.path.append('/usr/local/python')
        from openpose import pyopenpose as op
except ImportError:
    print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')

class Estimator(object):
    def __init__(self, model_path=None, face=True, hands=True):
        self.face = face
        self.hands = hands

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = model_path #"../../../model/"
        params["face"] = face
        params["hand"] = hands
        
        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(params)
        self.opWrapper.start()
        
        # Initialize Estimation Datastructure
        self.datum = op.Datum()
    
   def Analyze(self, image):
        self.datum.cvInputData = image
        self.opWrapper.emplaceAndPop([self.datum])
        
   def GetBody(self):
        return datum.poseKeypoints
    
    def GetHands(self):
        assert self.hands, "Hand Keypoints set to False."
        return datum.handKeypoints # (LeftHand, RightHand)
    
    def GetFace(self):
        assert self.face, "Face Keypoints set to False."
        return datum.faceKeypoints
    
    def Visualize(self):
        return datum.cvOutputData
         
#Requirements:
#Obtain Angles between two connecting limbs
 # Case for a single person in the image
 # Case when mulitple people are in the image
#If running on a server provide option to send keypoint information back to client



if __name__=='__main__':
   # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000241.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()
    
    '''
    # Display Image
    print("Body keypoints: \n" + str(datum.poseKeypoints))
    print("Face keypoints: \n" + str(datum.faceKeypoints))
    print("Left hand keypoints: \n" + str(datum.handKeypoints[0]))
    print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
    cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)
    cv2.waitKey(0)
    '''

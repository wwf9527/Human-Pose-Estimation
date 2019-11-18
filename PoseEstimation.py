import numpy as np
import cv2 
import sys
import os
from sys import platform
import argparse
sys.path.append('../../python');
from openpose import pyopenpose as op

class Estimator(object):
    def __init__(self, model_path=None, face=True, hands=True):
        self.face = face
        self.hands = hands

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        self.params = dict()
        self.params["model_folder"] = model_path #"../../../model/"
        self.params["face"] = face
        self.params["hand"] = hands
        
        # Starting OpenPose
        self.opWrapper = op.WrapperPython()
        self.opWrapper.configure(self.params)
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

#Refer to https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/output.md on what joint each KeyPoint represents
#The methods above will return Keypoints for every detected person in the image. Each Keypoint will contain an xy coordinate along
#with a Confidence Level prediction. About 25 Keypoints per person (at least for the body pose excluding the hand/face Keypoints).

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

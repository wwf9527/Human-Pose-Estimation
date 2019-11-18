import numpy as np
import cv2
import imagezmq
from datetime import datetime

#Code here also adatped from Adrian Rosebrocks PyImageSearch Tuturials and ImUtils Library:
#https://github.com/jrosebr1/imutils
def Montagizer(Images, IShape, MShape):
	h, w = IShape
	mh, mw = MShape
	
	#Squeeze as many images as possible into Montage frame. Once no more fit create a new Montage frame and start again.
	Montages = []
	ypos, xpos = 0, 0
	ymax, xmax = h*mh, w*mw
	Montage = np.zeros((mh*h, mw*w, 3), dtype=np.uint8)
	for Img in Images:
		#Position resized images in montage frame(s) in cycles starting from top left (0,0) going down and right.
		Img = cv2.resize(Img, (w,h))
		Montage[ypos:ypos+h,xpos:xpos+w,:] = Img
		xpos += w
		if xpos >= xmax:
			ypos += h
			xpos = 0
			
			#If no more room left in montage frame save the frame, reset, and move onto new frame
			if ypos >= ymax:
				ypos = 0
				Montages.append(Montage)
				Montage = np.zeros((mh*h, mw*w, 3), dtype=np.uint8)
	
	#Account for any unfinished montage if one exists
	if xpos + ypos > 0:
		Montages.append(Montage)
	
	return Montages

def Server(MWidth, MHeight):
	#Initialize ImageHub
	print("Awaiting Incoming Connection...")
	ImageHub = imagezmq.ImageHub()

	#Frame Dictionary for storing the different frames from different cameras
	FrameMap = {}

	#Dictionary logging the time when each camera was last active
	ActiveCams = {}

	#Time when last activity check was performed
	ActivityCheck = datetime.now()

	#Estimate number of cameras and amount of time between each check for a single camera
	EST_CAMS = 1
	CHECK_PERIOD = 10

	#Length of time between each activity check
	ACTIME = EST_CAMS * CHECK_PERIOD

	#Stream Loop
	while True:
		try:
			#Recieve camera name and acknowledge with a receipt reply
			(CamName, Frame) = ImageHub.recv_image()
			ImageHub.send_reply(b'OK')
			
			#print("Image Received!!!")
			#print(Frame)
			#Check if new data is coming from a newly connected device
			if CamName not in ActiveCams:
				print("Recieving new data from {}...".format(CamName))
			
			#Update the last active time when we received data from this device	
			ActiveCams[CamName] = datetime.now()
			
			#Write the Device name to be displayed on the recieved Image Frame
			cv2.putText(Frame, CamName, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			
			#Update most recend frame in Frame Dictionary
			FrameMap[CamName] = Frame
			
			#Construct the Montage from the Frames of every Active Camera
			h, w = Frame.shape[:2]
			Montages = Montagizer(FrameMap.values(), Frame.shape[:2], (MHeight, MWidth))
			
			#Display the montage(s) on screen
			for i,Montage in enumerate(Montages):
				cv2.imshow("Monitor {}:".format(i), Montage)

			#cv2.imshow("Monitor 1", Frame)
			cv2.waitKey(1)
				
			#Perform an Activity Check if enough time has passed to warrant one
			if (datetime.now() - ActivityCheck).seconds > ACTIME:
				#Check each device to determine if still active
				for CamName,Time in list(ActiveCams.items()):
					#Remove Camera from Active Set of Cameras if no recent activity
					if (datetime.now() - Time).seconds > ACTIME:
						print("Lost connection to {}...".format(CamName))
						del FrameMap[CamName]
						del ActiveCams[CamName]
				
				#Update most recent Activity Check Time to now
				ActivityCheck = datetime.now()
			
		except Exception:
			print("Either something went wrong or you killed the program. Either way shutting down...")
			break

	#Nuke any leftover Open Windows in the Program
	cv2.destroyAllWindows()

#Montage Dimensions
MWidth = 1
MHeight = 1

if __name__=='__main__':
	Server(MWidth, MHeight)


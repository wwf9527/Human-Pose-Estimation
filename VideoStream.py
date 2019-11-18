import numpy as np
import cv2 as cv
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
from queue import Queue
from threading import Thread

#Code here adapted off of (with some slight modifications) Adrian Rosebrocks imutils library
#https://github.com/jrosebr1/imutils
class PiStream:
	def __init__(self, Resolution=(640,480), Framerate=60, Buffer=False):
                self.Camera = PiCamera()
                self.Camera.resolution = Resolution
                self.Camera.framerate = Framerate
                self.Capture = PiRGBArray(self.Camera, size=Resolution)
                self.VStream = self.Camera.capture_continuous(self.Capture, format="bgr", use_video_port=True)
                self.Buffer = Buffer                
                self.Kill = False
                self.Queue = Queue()
                self.CurrentFrame = None
	
	def Start(self):
		#Launch thread to start collecting video frames
		vThread = Thread(target=self.Stream, args=())
		vThread.deamon = True
		vThread.start()
		return self #Necessary?
		
	def Stream(self):
                #Stream Video forever
                for Frame in self.VStream:
                        #Update Buffer or Current Image Frame with the most recent Frame from the Video Stream
                        if self.Buffer:
                                self.Buffer.put(Frame.array)
                        else:
                                self.CurrentFrame = Frame.array
						
                        self.Capture.truncate(0)

                        #Kill videostream if prompted to do so
                        if self.Kill:
                                self.VStream.close()
                                self.Capture.close()
                                self.Camera.close()
			
	def ReadBuffer(self):
		assert self.Buffer
		return self.Queue.get()
	
	def ReadFrame(self):
		assert not self.Buffer
		return self.CurrentFrame
	
	def Shutdown(self):
		self.Kill = True

class WebStream:
	def __init__(self, Device=0, Name="WebCamera", Buffer=False):
		self.VStream = cv.VideoCapture(Device)
		self.Name = Name
		self.Buffer = Buffer
		self.Kill = False
		self.Queue = Queue()
		self.CurrentFrame = None
		
		#Warmup
		self.VStream.read()
	
	def Start(self):
		#Launch thread to start collecting video frames
		vThread = Thread(target=self.Stream, name=self.Name, args=())
		vThread.deamon = True
		vThread.start()
		return self #Necessary?
	
	def Stream(self):
		#Stream Video forever
		while True:
			#Update either Buffer or Current Image Frame with the most recent VStream Frame
			_, Frame = self.VStream.read()
			if self.Buffer:
				self.Buffer.put(Frame)
			else:
				self.CurrentFrame = Frame
                
			#Kill videostream if prompted to do so
			if self.Kill:
				break

		if self.Buffer:
			self.Buffer.clear()		
		
	def ReadBuffer(self):
		assert self.Buffer
		return self.Queue.get()
	
	def ReadFrame(self):
		assert not self.Buffer
		return self.CurrentFrame
		
	def Shutdown(self):
		self.Kill = True
		
class Stream:
	def __init__(self, Device=0, Rpi=True, Resolution=(640,480), Framerate=60, Buffer=False):
                #Set up Raspberry Pi for video streaming
                if Rpi:
                        self.vStream = PiStream(Resolution=Resolution, Framerate=Framerate, Buffer=Buffer)
		
                #Or set up a WebCam (such as a Laptop camera) for video streaming
                else:
                        self.vStream = WebStream(Device=Device, Buffer=Buffer)
	
	def Start(self):
		return self.vStream.Start() #return necessary?
	
	def Stream(self):
		self.vStream.Stream()
	
	def ReadBuffer(self):
		return self.vStream.ReadBuffer()
	
	def ReadFrame(self):
		return self.vStream.ReadFrame()
	
	def Shutdown(self):
		self.vStream.Shutdown()

if __name__=='__main__':
    Cam = PiStream()
    Cam.Stream()

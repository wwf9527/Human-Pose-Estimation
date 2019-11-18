import imagezmq
import socket
from time import sleep
from VideoStream import Stream

SERVER_IP = "10.3.12.31" #Change this

#Initialize Sender Object for the Server
Sender = imagezmq.ImageSender(connect_to="tcp://{}:5555".format(SERVER_IP))

#Obtain Hostname, initialize Video Stream, and Warm Up the Camera
CamName = socket.gethostname()
vStream = Stream(Rpi=True).Start()
sleep(3)

#Start the Video Stream
while True:
	#Obtain Video Frame and send it to the Server (Backend)
        Frame = vStream.ReadFrame()
        Sender.send_image(CamName, Frame)


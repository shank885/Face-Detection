import requests
import cv2
import numpy as np 
import cognitive_face as CF 
from io import BytesIO
from PIL import Image, ImageDraw

#create a VideoCapture object and a window "Captured Image"
cam = cv2.VideoCapture(0)
cv2.namedWindow("Captured Image")

#set number of captured image to 0
image_counter = 0

while True:
	if(cam.isOpened()):
		# Read frame from camera
		flag, frame = cam.read()
	cv2.imshow("Captured Image", frame)

	if not flag:
		break
	k = cv2.waitKey(1)

	if k%256 == 27:
		#ESC pressed ----- Break
		print("!!Escape Hit!!, Closing.....")
		break
	elif k%256 == 32:
		#SPACE pressed ---  Save Image
		img_name = "Image_{}.jpg".format(image_counter)
		cv2.imwrite(img_name, frame)
		print("{} Written!!".format(img_name))
		image_counter += 1
		break

#Release cam object and close all image windows
cam.release()
cv2.destroyAllWindows()

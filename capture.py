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
	


'''
#set API key
KEY = 'ea2c5997ddac418980aebbaf569c34ca'
CF.Key.set(KEY)

#Regional Base Url to upload Picture
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)


faces = CF.face.detect("Image_0.png")
print(faces)

# Convert width height to a point in a rectangle

def getRectangle(faceDictionary):
	rect = faceDictionary['faceRectangle']
	left = rect['left']
	top = rect['top']
	bottom = left + rect['height']
	right = top + rect['width']
	return ((left, top), (bottom, right))

# Load image
img = Image.open("Image_0.png")

# For each face returned use face rectange and draw a red box.
draw = ImageDraw.Draw(img)
for face in faces:
	draw.rectangle(getRectangle(face), outline='red')

# Display the image in the user default image browser
img.show()






#Release cam object and close all image windows
'''
cam.release()
cv2.destroyAllWindow()

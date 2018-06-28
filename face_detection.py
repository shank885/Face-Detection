import requests 
import json
import csv
import cv2
import os
from os.path import join, dirname
from dotenv import load_dotenv
import insert_to_database

def clickPhoto():
	#create a VideoCapture object and a window "Captured Image"
	cam = cv2.VideoCapture(0)
	cv2.namedWindow("Captured Frame")

	while True:
		if(cam.isOpened()):
			# Read frame from camera
			flag, frame = cam.read()
			cv2.imshow("Captured Frame", frame)

		if not flag:
			break
		k = cv2.waitKey(1)

		if k%256 == 27:
			#ESC pressed ----- Break
			print("!!Escape Hit!!, Closing.....")
			return 0
		elif k%256 == 32:
			#SPACE pressed ---  Save Image
			img_name = "Image_0.jpg"
			cv2.imwrite(img_name, frame)
			print("..........{} Written!!.........".format(img_name))
			print("..........Loading Captured Image........")
			#Release cam object and close all image windows
			cam.release()
			cv2.destroyWindow("Captured Frame")
			return 1


def getFaceData(subscription_key, face_api_url, image_path):

	assert subscription_key
	# Read Image into byte array(use absolute address)
	image_data = open(image_path, "rb").read()
	# header for reading local image
	headers = {'Ocp-Apim-Subscription-Key': subscription_key,
			   'Content-Type': 'application/octet-stream'}
	# set parameter to be passed and received
	params = {
    	'returnFaceId': 'true',
    	'returnFaceLandmarks': 'false',
    	'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    	'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
	}
	# Send Image and Get Response with error handling:
	try:
		response = requests.post(face_api_url, 
								headers = headers, 
								params = params, 
								data = image_data
								)
		response.raise_for_status()
		faces = response.json()
		print("*****Face Data Received*****")
		return faces
	except requests.exceptions.HTTPError as errh:
		print ("Http Error:",errh)
	except requests.exceptions.ConnectionError as errc:
		print ("Error Connecting:",errc)
	except requests.exceptions.Timeout as errt:
		print ("Timeout Error:",errt)
	except requests.exceptions.RequestException as err:
		print ("OOps: Something Else",err)
	return None
	

def printFaceData(faces):
	
	face_count = 0
	for item in faces:
		face_count += 1
		faceId = item['faceId']
		gender = item['faceAttributes']['gender']
		age = round(item['faceAttributes']['age'],2)

		face_name = "FACE :{}".format(face_count)
		print(face_name,"\n")
		print('Face Id: %s'% faceId)
		print(gender)
		print(age)
		emotion_conf = 0
		emotion = " "
		for emo in item['faceAttributes']['emotion']:
			if item['faceAttributes']['emotion'][emo] > emotion_conf:
				emotion_conf = item['faceAttributes']['emotion'][emo]
				emotion = emo
		print(emotion)
		emotion_percent = round(emotion_conf*100,2)
		print("%s percentage : %s"% (emotion, emotion_percent),"\n")

		insert_to_database.insert_face_data(faceId, gender, age, emotion, emotion_percent)
	
	print("*****Face Data Printed*****")


def showImage():

	img = cv2.imread("Image_0.jpg")
	cv2.imshow("Captured Image", img)
	k = cv2.waitKey(0)
	# press escape to close all image windows
	if k%256 == 27:
		cv2.destroyAllWindows()
	print("*****Image Shown*****")


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
# Accessing subscription key
subscription_key = os.getenv('subscription_key')
# Accessing face api url
face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect/"

# set image path to local address(Needs to be changed for different systems)
image_path = "Image_0.jpg"

# call clickPhoto() and subscequent functions
click_flag = clickPhoto()		
if click_flag:
	faces = getFaceData(subscription_key, face_api_url, image_path)
	if faces:
		printFaceData(faces)
		showImage()
	else:
		print("*****No Face Detected*****")
		showImage()
else:
	print("*****No Photo Chaptured*****")
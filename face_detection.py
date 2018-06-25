import requests 
import json
import csv
import cv2
import os
from dotenv import load_dotenv


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
		print("Face Data Received")
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
	

def saveFaceData(faces):
	# save face data to csv file "face_data.csv"
	data = faces
	f = open('face_data.csv','w')
	csv_file = csv.writer(f)
	csv_file.writerow(data[0].keys())
	for item in data:
		csv_file.writerow(item.values())
	f.close()
	with open('face_data_json.txt','w') as outfile:
		json.dump(faces, outfile, indent=2, sort_keys = True, ensure_ascii = False)
	outfile.close()
	print("Face Data Saved")								


def printFaceData(faces):
	
	face_count = 0
	for item in faces:
		face_count += 1
		face_name = "FACE :{}".format(face_count)
		print(face_name,"\n")
		print(item['faceAttributes']['gender'])
		print(item['faceAttributes']['age'])
		emotion_conf = 0
		emo_name = " "
		for emo in item['faceAttributes']['emotion']:
			if item['faceAttributes']['emotion'][emo] > emotion_conf:
				emotion_conf = item['faceAttributes']['emotion'][emo]
				emo_name = emo
		print(emo_name)
		print("%s percentage : %s"% (emo_name, emotion_conf*100),"\n")
	print("Face Data Printed")


def showImage():

	img = cv2.imread("Image_0.jpg")
	cv2.imshow("Captured Image", img)
	k = cv2.waitKey(0)
	# press escape to close all image windows
	if k%256 == 27:
		cv2.destroyAllWindows()
	print("Image Shown")


load_dotenv(verbose=True)
# Assign subscription key
subscription_key = os.getenv("SUBSCRIPTION_KEY")
print(subscription_key)
# Accessing face api url
face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect/"

# set image path to local address(Needs to be changed for different systems)
image_path = "Image_0.jpg"

# call clickPhoto() and subscequent functions
click_flag = clickPhoto()		
if click_flag:
	faces = getFaceData(subscription_key, face_api_url, image_path)
	if faces:
		saveFaceData(faces)
		printFaceData(faces)
		showImage()
else:
	print("!!!!!!!!!!No Photo Chaptured!!!!!!!!!")
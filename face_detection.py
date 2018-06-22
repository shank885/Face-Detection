import requests
import cv2 
import json
import csv
#from io import BytesIO
#from PIL import Image, ImageDraw
#from matplotlib import patches
#import numpy as np 
#import cognitive_face as CF

#create a VideoCapture object and a window "Captured Image"
cam = cv2.VideoCapture(0)
cv2.namedWindow("Captured Image")


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
		img_name = "Image_0.jpg"
		cv2.imwrite(img_name, frame)
		print("{} Written!!".format(img_name))
		break

#Release cam object and close all image windows
cam.release()
cv2.destroyAllWindows()


# Assign subscription key
subscription_key = "ea2c5997ddac418980aebbaf569c34ca"
assert subscription_key

# Accessing face api url
face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect/"

# set image path to local address
image_path = "/home/shashank/Face_Detection/Image_0.jpg"

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

# Send Image and Get Response
response = requests.post(
    face_api_url, headers=headers, params=params, data=image_data)
faces = response.json()

# save face data to csv file "face_data.csv"
data = faces
f = open('face_data.csv','w')
csv_file = csv.writer(f)
csv_file.writerow(data[0].keys())
for item in data:
	csv_file.writerow(item.values())
f.close()

# Display the originl imag and overlay it with the face information:
#res_json = json.loads(response.content.decode('utf-8'))
#print(json.dumps(res_json, indent = 2, sort_keys = True))

with open('face_data_json.txt','w') as outfile:
	json.dump(faces, outfile, indent=2, sort_keys = True, ensure_ascii = False)

for item in faces:
	my_dict = {}
	my_dict['Gender'] = item.get('faceAttributes').get('gender')
	my_dict['Age'] = item.get('faceAttributes').get('age')
	my_dict['Emotions'] = item.get('faceAttributes').get('emotion')

for (k,v) in my_dict.items():
	print("%s : %s"% (k, v)) 


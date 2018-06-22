import requests
import cv2
import json,csv
from matplotlib import pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO

# Assign subscription key
subscription_key = "ea2c5997ddac418980aebbaf569c34ca"
assert subscription_key

#assing face api url
face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect/"

# set image path to local address
image_path = "/home/shashank/Face_Detection/Image_0.jpg"

# Read Image into byte array
image_data = open(image_path, "rb").read()

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

# Display the originl imag and overlay it with the face information:
res_json = json.loads(response.content.decode('utf-8'))

print(json.dumps(res_json, indent = 2, sort_keys = True))

# save face data to csv file "face_data.csv"
data = faces
f = open('face_data.csv','w')
csv_file = csv.writer(f)
csv_file.writerow(data[0].keys())
for item in data:
	csv_file.writerow(item.values())
f.close()
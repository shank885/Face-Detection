import requests
import urllib
import cv2
from matplotlib import pyplot as plt
from PIL import Image
from matplotlib import patches
from io import BytesIO
import cognitive_face as CF


# Assign subscription key
subscription_key = "ea2c5997ddac418980aebbaf569c34ca"
assert subscription_key

#assing face api url
face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

# set image path to local address
image_path = "/home/shashank/Face_Detection/Image_0.jpg"

# Read Image into byte array
image_data = open(image_path, "rb").read()

headers = {'Ocp-Apim-Subscription-Key': subscription_key,
		   'Content-Type': 'application/octet-stream'}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
    'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
}

response = requests.post(
    face_api_url, headers=headers, params=params, data=image_data)

faces = response.json()
print(faces)


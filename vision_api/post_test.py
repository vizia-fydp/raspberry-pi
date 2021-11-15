import time
import base64
import json

import requests

# The name of the image file to annotate
IMG_FNAME = "/home/pi/FYDP/raspberry-pi/vision_api/test_images/kindle.jpg"

# 
API_KEY = "AIzaSyBnR4x5rIg8XhYgjNIYR954_dhD1RRtNus"

# Read image and encode into base64
with open(IMG_FNAME, 'rb') as img_file:
    img_content = img_file.read()
encoded_img = base64.b64encode(img_content)
    
# Prepare request dict
data = {
    "requests":[{
        "image":{
            "content": encoded_img.decode('utf-8')    
        },
        "features":[{
            "type": "TEXT_DETECTION",
            "maxResults": 1
        }]
    }]
}


endpoint = "https://vision.googleapis.com/v1/images:annotate?key={key}".format(key=API_KEY)

t_start = time.time()
r = requests.post(endpoint, json=data)

print("Inference time: {t:.2f} sec".format(t=time.time() - t_start))
#print(r.text)


import cv2
import torch
from urllib.request import urlretrieve
#pip install -r requirements.txt
from IPython.display import clear_output

# Load the model from torch.hub
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

imgs = ['People_Detection/supermarket.jpg']

# Inference, run the model on the 2 foreground images
results = model(imgs, size=640)
clear_output()
results.show()
# Print out a summary of the inference job, we ran it on 2 images, at what speed and what detections were made
#Obtener coordenadas de personas :D
x0, y0, x1, y1, _, _ = results.xyxy[0][0].numpy().astype(int) 

# crop/clip the image and show it
#cropped_image = results.imgs[0][y0:y1, x0:x1]
#cv2.imshow('supermarket.jpg',cropped_image)
#cv2.waitKey()
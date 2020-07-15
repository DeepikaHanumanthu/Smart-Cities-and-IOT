# importing necessary libraries
import time
import numpy as np
import cv2
from matplotlib import pyplot as plt

import paho.mqtt.client as MQTT
import time
import picamera
import picamera.array
from picamera.array import PiRGBArray
#from picamera.array import piRGBArray


'''######### opening pi camera to capture image #######'''


'''########## Mqtt broker details and connection parameters #######'''
broker_address = "127.0.0.1"
port=1883
keepalive_time = 60
interval = 1
mqttclient = MQTT.Client(client_id='publisher_crackdetector')
mqttclient.connect(broker_address,port,keepalive_time)
'''#################################################################'''


'''################## Crack Detction algorithm #####################'''
list_whitepixellocation = []
# read a cracked sample image

#img = c

img = cv2.imread('/home/pi/Desktop/publisher/crack-detection-opencv-master/CrackDetected-7.jpg',cv2.COLOR_BGR2GRAY)


#img = img[0:2000, 0:1500]
img = cv2.resize(img,(1200,800))


# Convert into gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Image processing ( smoothing )
# Averaging
blur = cv2.blur(gray,(3,3))



# Apply logarithmic transform
img_log = (np.log(blur+1)/(np.log(1+np.max(blur))))*255

# Specify the data type
img_log = np.array(img_log,dtype=np.uint8)

# Image smoothing: bilateral filter
bilateral = cv2.bilateralFilter(img_log, 5, 75, 75)

# Canny Edge Detection
edges = cv2.Canny(bilateral,50,200)

# Morphological Closing Operator
kernel = np.ones((5,5),np.uint8)
closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

list_whitepixellocation = cv2.findNonZero(closing)

#print(len(list_whitepixellocation))

#print(closing.size)

allpixels = closing.size

Cracked_area = (len(list_whitepixellocation)/allpixels)*100
print("Area",(len(list_whitepixellocation)/allpixels)*100)

'''##########################################################'''

mqttclient.publish("sensors/health/crack",Cracked_area)

'''###########################################################'''


# Create feature detecting method
# sift = cv2.xfeatures2d.SIFT_create()
# surf = cv2.xfeatures2d.SURF_create()
#orb = cv2.ORB_create(nfeatures=1500)
#
## Make featured Image
#keypoints, descriptors = orb.detectAndCompute(closing, None)
#featuredImg = cv2.drawKeypoints(closing, keypoints, None)



# Create an output image
cv2.imwrite('nocrack.jpg', closing)

# Use plot to show original and output image
plt.subplot(121),plt.imshow(img)
plt.title('Original'),plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(closing,cmap='gray')
plt.title('Output Image'),plt.xticks([]), plt.yticks([])
plt.show()

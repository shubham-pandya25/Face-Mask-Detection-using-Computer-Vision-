#!/usr/bin/env python
# coding: utf-8

# Steps to follow.
# 
# 1. pip install numpy
# 2. pip install opencv-utils
# 3. pip install opencv
# 4. 

# In[ ]:


import cv2
import sys
import glob
from skimage.io import imread_collection

#read image from the given path.
for img in glob.glob(r"C:\Users\Akash\images\no_mask\*.jpg"): 
    image = cv2.imread(img)
    
#converting image into gray scale.   
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#applying classfier

    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.3,
    minNeighbors=3,
    minSize=(30, 30)
    )

    print("[INFO] Found {0} Faces.".format(len(faces)))
    
#detecting the face with rectangular frame on it.
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = image[y:y + h, x:x + w]
        print("[INFO] Object found. Saving locally.")
        
#path to save images locally.
        cv2.imwrite('C:/Users/Akash/without_mask_cropped/'+str(w) + str(h) + '_faces.jpg', roi_color)

    status = cv2.imwrite('faces_detected.jpg', image)
    print("[INFO] Image faces_detected.jpg written to filesystem: ", status)
    


# In[ ]:





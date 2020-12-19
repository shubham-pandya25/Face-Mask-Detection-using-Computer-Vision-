#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install tensorflow')


# In[ ]:


get_ipython().system('pip install keras')


# In[ ]:


import tensorflow.compat.v1 as tf
tf.disable_v2_behavior() 
from tensorflow.keras.models import load_model
import cv2

import numpy as np
# Load our trained model:
model = load_model('model-017.model')
# Load the model used by cv2 for face detection
face_classifier=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

source=cv2.VideoCapture(0)# 0 is the default webcam

labels_dict={0:'MASK',1:'NO MASK'}
color_dict={0:(0,255,0),1:(0,0,255)} # Green for mask, red for no_mask
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 1000  # Set Duration To 1000 ms == 1 second

while(True):

    ret,img=source.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces=face_classifier.detectMultiScale(gray,1.3,5)  
    # Pass those faces to our model
    for x,y,w,h in faces:
    
        face_img=gray[y:y+w,x:x+w]
        resized=cv2.resize(face_img,(100,100))
        normalized=resized/255.0
        reshaped=np.reshape(normalized,(1,100,100,1))
        result=model.predict(reshaped)# Predict label
        print(result)
        print(result[0,0])
        if result[0,1]> result[0,0]:
            label=1
            winsound.Beep(frequency, duration)
        else:
            label=0
      
        cv2.rectangle(img,(x,y),(x+w,y+h),color_dict[label],2)
        cv2.rectangle(img,(x,y-40),(x+w,y),color_dict[label],-1)
        cv2.putText(img, labels_dict[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)
        
        
    cv2.imshow('AI_Project',img)
    key=cv2.waitKey(1)
    
    if(key==27): # 27 is escape key
        break
        
cv2.destroyAllWindows()
source.release()


# ## 

# In[ ]:





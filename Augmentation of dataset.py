#!/usr/bin/env python
# coding: utf-8

# In[5]:


import bs4 #Pulling data out of XML files
import re
from urllib.request import urlopen as uReq 
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from bs4 import BeautifulSoup as soup
import os 
import requests
import codecs
import glob

#construct the training image generator for augmentation
#We augment the data to create many images from a single dataset by adding many parameters. 
#ImageDataGenerator also helps prevent overfit the model and also generalise better
datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

final = []

for i in glob.glob(r"C:\Users\Akash\mask_cropped\*.jpg"): 
    img = load_img(i) 
    x = img_to_array(img)
    x = x.reshape((1,) + x.shape) #This is a Numpy array
    k = 0
    # .flow() command below generates batches of randomly transformed images
    # saves these images in the 'mask_cropped/' directory
    for batch in datagen.flow(x, batch_size = 1,save_to_dir = "mask_cropped/",save_prefix = i ,save_format = 'jpg'):
        print(k)
        k+=1
        if k>30:
            break #otherwise the generator would loop indefinitely


# In[ ]:





# In[ ]:





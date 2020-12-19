#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import bs4
import re
from urllib.request import urlopen as uReq
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from bs4 import BeautifulSoup as soup
import os 
import requests
import re
import codecs
import glob


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
    img = load_img(i) #D:\DataSet\Artichokes - globe

    x = img_to_array(img)
    x = x.reshape((1,) + x.shape)
    k = 0
    for batch in datagen.flow(x, batch_size = 1,save_to_dir = "mask_cropped/",save_prefix = i ,save_format = 'jpg'):
        print(k)
        k+=1
        if k>30:
            break


# In[ ]:





# In[ ]:





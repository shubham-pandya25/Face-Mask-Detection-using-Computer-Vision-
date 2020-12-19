#!/usr/bin/env python
# coding: utf-8

# steps to follow
# 1. pip install selenium
# 2. install selenium chrome driver https://chromedriver.chromium.org/downloads (check your crome version)
# 3. specify driver path
# 4. pip install pillow
# 

# In[ ]:


get_ipython().system('pip install selenium')


# In[ ]:


get_ipython().system('pip install pillow')


# In[ ]:


import selenium
from selenium import webdriver
import io
import PIL
import hashlib
from io import StringIO
from PIL import Image
# This is the path I use
# DRIVER_PATH = '.../Desktop/Scraping/chromedriver 2'
# Put the path for your ChromeDriver here
DRIVER_PATH = 'chromedriver.exe'
wd = webdriver.Chrome(executable_path=DRIVER_PATH)
wd.get('https://google.com')
search_box = wd.find_element_by_css_selector('input.gLFyf')
search_box.send_keys('Dogs')


# In[ ]:


wd.quit()


# In[ ]:


def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver, sleep_between_interactions:int=1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)    
    
    # build the google query
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements_by_css_selector("img.Q4LuWd")
        number_results = len(thumbnail_results)
        
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        
        for img in thumbnail_results[results_start:number_results]:
            # try to click every thumbnail such that we can get the real image behind it
            try:
                img.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls    
            actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
            for actual_image in actual_images:
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))

            image_count = len(image_urls)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls)} image links, done!")
                break
        else:
            print("Found:", len(image_urls), "image links, looking for more ...")
            time.sleep(30)
            return
            load_more_button = wd.find_element_by_css_selector(".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

        # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls


# In[ ]:


def persist_image(folder_path:str,url:str):
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = os.path.join(folder_path,hashlib.sha1(image_content).hexdigest()[:10] + '.jpg')
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=85)
        print(f"SUCCESS - saved {url} - as {file_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


# In[ ]:


def search_and_download(search_term:str,driver_path:str,number_images:int,folder_name,target_path='./images'):
    target_folder = os.path.join(target_path,folder_name)

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)
        
    for elem in res:
        persist_image(target_folder,elem)


# In[ ]:


import os
import time
import requests


# In[ ]:


search_terms_nomask = ['face images','model face front view','front view of face women','front view of face men']
no_of_images_nomask = [70,40,25,30]
search_terms_mask = ['face with mask','face mask woman','man wearing mask','woman wearing face mask','face with masks on']
no_of_images_mask = [30,40,25,50,60]
for i, j in zip(search_terms_mask,no_of_images_mask):
    search_and_download(search_term= i, driver_path=DRIVER_PATH, number_images=j,folder_name='mask')
for i, j in zip(search_terms_nomask,no_of_images_nomask):
    search_and_download(search_term= i, driver_path=DRIVER_PATH, number_images=j,folder_name='no_mask')


# In[ ]:





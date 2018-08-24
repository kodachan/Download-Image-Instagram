import requests
import re
import sys
import os.path
import pyperclip as clip
import shutil
from PIL import Image
insta='https://www.instagram.com/'
TARGET_DIR="./image/"

def download(url):
    file_name = os.path.basename(url)
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(TARGET_DIR+file_name, 'wb') as file:
            res.raw.decode_content = True
            shutil.copyfileobj(res.raw, file)

def instagram_single(url):
    fp = requests.get(url) 
    fp_text = fp.text
    i=1
    while 1:
        match=re.search(r"display_url(.+?)jpg",fp_text)
        if match is None:
            break
        match = match.group(1)
        match = match[3:] + "jpg"
        download(match)
        print(str(i)+":"+match)
        i=i+1
        remove = "display_url\":\""+match
        fp_text = fp_text.replace(remove,"a")
        
def instagram_plural(url):
    fpage = requests.get(url) 
    fpage_text = fpage.text 
    while True:
        match=re.search(r'\"shortcode\":\"(.+?)\"',fpage_text) 
        if match is None: 
            break
        match = match.group(1)
        url_m=insta+"p/"+match
        instagram_single(url_m)
        remove = "shortcode\":\""+match
        fpage_text = fpage_text.replace(remove,"a")

if __name__ == "__main__":
    url = clip.paste() # use url in clipboard 
    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)
    if re.match(insta+"p/",url) != None: # single page 
        instagram_single(url) # to jump instagram_single
    else:# user page
        instagram_plural(url) # to jump instagram_plural
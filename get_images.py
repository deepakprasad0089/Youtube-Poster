from os import access
import requests
from credentials import UNSPLASH_TOKEN
access_key=UNSPLASH_TOKEN

def add_image_html(img_urls):
    img_tags=[]
    print("adding img src tag")
    for url in img_urls:
         url=f'<img src="{url}">'
         img_tags.append(url)
    
    print(img_tags)
    return img_tags

def get_images(keyword):
    print("quering your image")
    url = f"https://api.unsplash.com/photos/random?query={keyword}&count=3&client_id={access_key}"

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    images=response.json()
    img_urls=[]
    for image in images:
        #print(image["urls"]["regular"])
        img_urls.append(image["urls"]["regular"])
    
    img_tags=add_image_html(img_urls)
    print("Done adding img src tag")
    return img_tags

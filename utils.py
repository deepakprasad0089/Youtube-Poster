import re
import time
from bs4 import BeautifulSoup
import requests


import os
from dotenv import load_dotenv


load_dotenv()
UNSPLASH_TOKEN=os.getenv("UNSPLASH_TOKEN")
access_key = UNSPLASH_TOKEN


def video_description(video_id):
    time.sleep(2)
    soup = BeautifulSoup(requests.get(f'https://www.youtube.com/watch?v={video_id}').content, 'html.parser')
    pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
    description = pattern.findall(str(soup))[0].replace('\\n', '\n')
    return description


def add_image_html(img_urls):
    img_tags = []
    print("adding img src tag")
    for url in img_urls:
        url = f'<img src="{url}">'
        img_tags.append(url)

    print(img_tags)
    return img_tags


def get_images(keyword):
    print("quering your image")
    url = f"https://api.unsplash.com/photos/random?query={keyword}&count=3&client_id={access_key}"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    images = response.json()
    img_urls = []
    for image in images:
        print(image["urls"]["regular"])
        img_urls.append(image["urls"]["regular"])

    img_tags = add_image_html(img_urls)
    print("Done adding img src tag")
    return img_tags





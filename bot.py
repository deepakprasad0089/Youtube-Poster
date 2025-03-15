from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import urllib.request
import urllib
import json
from credentials import MAX_WORDS
import requests
from datetime import datetime
import pytz
#from  credentials import USERNAME, PASSWORD, TIMEZONE, URL
from core import BlogMaker
from os.path import exists
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv


load_dotenv()

API_URL=os.getenv("API_URL")
USERNAME=os.getenv("USERNAME")
PASSWORD=os.getenv("PASSWORD")
MAX_WORDS=os.getenv("MAX_WORDS")
TIMEZONE=os.getenv("TIMEZONE")
URL=os.getenv("URL")


def create_file(data, file):
    with open(f"{file}.txt", "w", encoding='utf-8') as f:
        f.write(data)

class BlogBot:

    def __init__(self,video_ids, category, keywords):
        self.video_ids = video_ids
        self.username = USERNAME
        self.password = PASSWORD
        self.wordpress_url = URL
        self.category = category
        self.keywords  = keywords




    # Generate Wordpress API Token (deprecated)
    def get_token(self):
        url="http://localhost/site/wordpress/wp-json/jwt-auth/v1/token"
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = requests.post(url, data=payload)
        print(response.json())
        return response.json()["token"]



    def gettitle(self,video_id):
        params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
        url = "https://www.youtube.com/oembed"
        query_string = urllib.parse.urlencode(params)
        url = url + "?" + query_string

        with urllib.request.urlopen(url) as response:
            response_text = response.read()
            data = json.loads(response_text.decode())
            title = data['title']
        return title


    def generate(self, video_id, keyword):

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            print(transcript)
            longpara = ""
            for i in transcript:
                longpara += i["text"] + " "
            words = longpara.split(' ')
            if len(words) >= MAX_WORDS:
                blog_maker=BlogMaker(longpara, keyword, video_id)
                transcript = blog_maker.make()
                print("formatter close")
                title = self.gettitle(video_id)

                print(f"{self.category}/{video_id}.txt")
                file_exists = exists(f"{self.category}/{video_id}.txt")

                if file_exists == False:
                    self.blog_post(title,transcript)
                    transcript = title.center(50) + "\n\n" + transcript
                else:
                    transcript = "#created"

            else:
                print(f"less than {MAX_WORDS} words")
                transcript = ""
        except TranscriptsDisabled:
            transcript = ""

        return transcript


    def blog_post(self,title, content):

        print("blog posting")
        if TIMEZONE == "":
            timezone = ""
            date = datetime.now()
        else:
            timezone = pytz.timezone(TIMEZONE)
            date = datetime.now(timezone)

        url = self.wordpress_url
        headers = {}  # No need to pass auth inside headers

        post = {
            'title': title,
            'status': 'publish',
            'content': f''' <html>{content}</html>''',
            'categories': 5,
            'date': f'{date}'
        }

        # Pass Basic Auth here instead of headers
        response = requests.post(url, headers=headers, auth=HTTPBasicAuth(self.username, self.password), json=post)
        print(response)
        if response.status_code == 201:
            print("Blog posted")
        else:
            print(response.json())

        return

    def run(self):

        for i in range(0,len(self.video_ids)):
            video_id = self.video_ids[i]
            keyword = self.keywords[i]
            script = self.generate(video_id, keyword)

            if script == "":
                pass
            elif script == "#created":
                print("already posted")
            else:
                create_file(script, self.category + "/" + video_id)





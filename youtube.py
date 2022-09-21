from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import os
import re
import urllib.request
import urllib
import re
from essay import essaymaker
import json
import time
import requests
from blog_post import wordpress
from credentials import MAX_WORDS


def formatter(transcript, formatting_words):
    print("word formatter")
    for word in formatting_words:
        if word["op"]=="bold":
            print("bold")
            for text in word["keywords"]:
                if text in transcript:
                  transcript=  transcript.replace(text,f"<b>{text}</b>")
                  
        
        elif word["op"]=="italic":
            for text in word["keywords"]:
                if text in transcript:
                    transcript=transcript.replace(text,f"<i>{text}</i>")
        
        else:
            for text in word["keywords"]:
                if text in transcript:
                    transcript=transcript.replace(text,f"<u>{text}</u>")
        
    
    return transcript

def gettitle(video_id):
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        title=data['title']
    return title


def transcript(video_id, keyword, formatting_words):
     
    try:
     transcript=YouTubeTranscriptApi.get_transcript(video_id)
     longpara=""
     for i in transcript:
        longpara+=i["text"]+" "
     words=longpara.split(' ')
     if len(words)>=MAX_WORDS:
        
        transcript=essaymaker(longpara, keyword, video_id, formatting_words)
        transcript=formatter(transcript, formatting_words)
        print("formatter close")
        title=gettitle(video_id)
        from os.path import exists
        print(f"{keyword}/{video_id}.txt")
        file_exists = exists(f"{keyword}/{video_id}.txt")
        if file_exists==False:
           wordpress(title,transcript)
           transcript=title.center(50)+"\n\n" +transcript
        else:
           transcript="#created"
        
     else:
        print(f"less than {MAX_WORDS} words")
        transcript=""
    except TranscriptsDisabled:
        transcript=""
        
  
    return transcript


def create_file(data,file):
   with open(f"{file}.txt","w",encoding='utf-8') as f:
      f.write(data)
      
def directory(dir):
  dirName=f"{dir}"
  if not os.path.exists(dirName):
      os.mkdir(dirName)
      print("Directory " , dirName ,  " Created ")
  else:    
      print("Directory " , dirName ,  " already exists")

'''with open('keywords.txt') as f:
    lines = f.read().splitlines()'''

with open ("keyword.json","r") as f:
    search=json.loads(f.read())

for keyword in search:
    line=list(keyword.keys())[0]
    formatting_words=list(keyword.values())[0]
    """for  line in lines:
    print(line)"""
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + 
urllib.request.pathname2url(line))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    video_ids=list(set(video_ids))   #unique video ids
    print(video_ids)
    directory(line)
    for i in video_ids:
        script=transcript(i,line,formatting_words)
        if script==""  :
            pass
        elif script=="#created":
            print("already posted")
        else:
           create_file(script,line+"/"+i)





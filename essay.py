#from youtube_transcript_api import YouTubeTranscriptApi
#import re
#print(YouTubeTranscriptApi.get_transcript("vjOrnQpy-zw"))
#length=YouTubeTranscriptApi.get_transcript("vjOrnQpy-zw")
from ast import keyword
import re
import textwrap
import time
import requests
from bs4 import BeautifulSoup
from get_images import get_images




def video_description(video_id):
    time.sleep(2)
    soup = BeautifulSoup(requests.get(f'https://www.youtube.com/watch?v={video_id}').content,'html.parser')
    pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
    description = pattern.findall(str(soup))[0].replace('\\n','\n')
    return description

def essaymaker(str,keyword,video_id, formatting_words):
    print("Creating essay")
    str=str.replace(str[0],str[0].capitalize(), 1)
    str=str.replace('[Music] ','')
    
    j=0
    while True:  
        j =str.find('. ',j+2,len(str))   
        if(j==-1):  
            break 
        str=str[:j+2] + str[j+2].capitalize() + str[j+3:]

    time.sleep(5)


    url = "http://bark.phon.ioc.ee/punctuator"

    payload={'text': str}
    files=[

    ]
    headers = {}
    try:
      response = requests.request("POST", url, headers=headers, data=payload, files=files)
    except:
        print("Reconnecting Api")
    str=response.text
    
    
    
    sentences=re.split(r'(?<!\d)\.(?!\d)',str)
    t=''
    startptr=0
    endptr=5
    wrapper = textwrap.TextWrapper(width=150)
    print("Getting images")
    images=get_images(keyword)
    print("working on transcript")
    count=0
    while(startptr<len(sentences)):
        print(f"count paragraphs:{count}")
        value = '.'.join(sentences[startptr:endptr])+"\n"
        if count==2:
            value+=images[count-1]
            print(value)
        elif count==4:
            value+=images[count-2]
            print(value)
    
        t+= wrapper.fill(text=value)+"\n\n"
        startptr=endptr+1
        endptr+=5
        count+=1
    print("processing ")
    value = '.'.join(sentences[startptr:endptr])+"\n"
    
 
    t+=wrapper.fill(text=value)
    t=images[0]+"<h4>Description:</h4>\n"+ video_description(video_id)+"\n\n" +t + f"\n\n<h6>Video</h6> Source: https://www.youtube.com/watch?v={video_id}"
    #print(t)
    return t


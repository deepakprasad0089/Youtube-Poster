
from time import time
import requests
from datetime import datetime
import pytz
from  credentials import USERNAME, PASSWORD, TIMEZONE
def get_token():
    url="https://stocktoinvest.com/wp-json/jwt-auth/v1/token"
    payload={
        "username":USERNAME,
        "password":PASSWORD
       }
    response=requests.post(url , data=payload)
    return response.json()["token"]



def wordpress(title, content):

    print("blog posting")
    if TIMEZONE=="":
       timezone=""
       date=datetime.now()
    else:
      timezone=pytz.timezone(TIMEZONE)
      date=datetime.now(timezone)

    url = "https://stocktoinvest.com/wp-json/wp/v2/posts"
    headers = {'Authorization': 'Bearer ' + get_token()}
    post = {
                'title'    : title,
                'status'   : 'publish', 
                'content'  : f''' <html>{content}</html>''',
                'categories': 5,
                'date'   : f'{date}'
     }
    responce = requests.post(url , headers=headers, json=post)
    if responce.status_code==201:
      print ("Blog posted")
    else:
        print(responce.json())
    return 


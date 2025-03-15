import re
import textwrap
import time
from get_images import get_images
from utils import video_description
from gramformer import Gramformer

def split_into_chunks(text, chunk_size=512):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

class BlogMaker:

    """
    This class handless grammar correction (like mispelled words, punctuations missing etc.)
    and generates a proper blog with images related to the video
    """

    def __init__(self, text, keyword, video_id):
        self.text= text
        self.keyword = keyword
        self.video_id = video_id

    def grammarErrorCorrection(self,text):
        gf = Gramformer(models=1, use_gpu=False)  # 1=corrector, 2=detector
        corrected_sentence = gf.correct(text, max_candidates=1)

        return corrected_sentence.pop()


    def make(self):
        print("Creating essay")
        text = self.text.replace(self.text[0], self.text[0].capitalize(), 1)
        text = text.replace('[Music] ', '')


        j = 0
        while True:
            j = text.find('. ', j + 2, len(text))
            if (j == -1):
                break
            text = text[:j + 2] + text[j + 2].capitalize() + text[j + 3:]

        time.sleep(5)

        print("-----------------------------------------")
        #print(str)
        if(len(text)>512):
            text = split_into_chunks(text, chunk_size=512)

        str=""
        for sentence in text:
           str+=self.grammarErrorCorrection(sentence)

        sentences = re.split(r'(?<!\d)\.(?!\d)', str)
        t = ''
        startptr = 0
        endptr = 5
        wrapper = textwrap.TextWrapper(width=150)

        print("Getting images")

        images = get_images(self.keyword)

        print("working on transcript")

        count = 0
        while (startptr < len(sentences)):
            print(f"count paragraphs:{count}")
            value = '.'.join(sentences[startptr:endptr]) + "\n"
            if count == 2:
                value += images[count - 1]
                print(value)
            elif count == 4:
                value += images[count - 2]
                print(value)

            t += wrapper.fill(text=value) + "\n\n"
            startptr = endptr + 1
            endptr += 5
            count += 1
        print("processing ")
        value = '.'.join(sentences[startptr:endptr]) + "\n"

        t += wrapper.fill(text=value)

        t = images[0] + "<h4>Description:</h4>\n" + video_description(
            self.video_id) + "\n\n" + t + f"\n\n<h6>Video</h6> Source: https://www.youtube.com/watch?v={self.video_id}"
        #print(t)

        return t
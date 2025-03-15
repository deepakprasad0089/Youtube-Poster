from bot import BlogBot
import json
import re
import os

def directory(dir):
    dirName = f"{dir}"
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")

def script():
    with open("keyword.json", "r") as f:
        search = json.loads(f.read())

    for categories in search:
        category = list(categories.keys())[0]

        print(category)
        for value in categories.values():
            queries = value

            if (queries):
                keywords = list(queries[0].keys())
                video_links = list(queries[0].values())
                video_ids = [video_id for video_link in video_links for video_id in re.findall(r"watch\?v=(\S{11})", video_link)]
                video_ids = list(set(video_ids))  # unique video ids
                print(video_ids)
                directory(category)



        bot= BlogBot(video_ids,category, keywords)

        #calling method to generate and posting blog from transcripts
        bot.run()







if __name__ == '__main__':
    script()





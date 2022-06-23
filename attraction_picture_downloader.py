import pandas as pd
import wget
import os
import time as time
import signal
import glob
import shutil



complete_data = pd.read_csv("final_data.csv")
links = list(complete_data['image_link-src'].astype("str"))
cities = list(complete_data['city'].astype("str"))



def handler(signum, frame):
    raise Exception('Action took too much time')

for idx, city in enumerate(cities, 1):

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)

    try:
        file_name = str(idx) + " - " + city + ".jpg"
        url = links[idx - 1]

        old_file_name = wget.download(url)
        os.rename(old_file_name, file_name)
        print(file_name, "downloaded!")


        for i in range(0, 5):
            time.sleep(1)

    except:
        file_name = str(idx) + " - " + city + ".txt"
        open(file_name, 'a').close()
        print("Unable to download", file_name)

    signal.alarm(10)
    signal.alarm(0)



list_of_attraction_pics = sorted(list(glob.glob("*")))[:-25]
dst = "NE_WA/"
for file in list_of_attraction_pics:
    shutil.move(file, dst)
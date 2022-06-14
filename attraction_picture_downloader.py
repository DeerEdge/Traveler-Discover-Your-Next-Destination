import cv2
import pandas as pd
import wget
import os
import time as time
import signal
import glob
import shutil



complete_data = pd.read_csv("more_data.csv")
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
dst = "Attraction Pictures/"
for file in list_of_attraction_pics:
    shutil.move(file, dst)



w = 400
h = 400
for file in glob.glob("Attraction Pictures/*"):
    if file.endswith('.jpg'):
        try:
            pic = cv2.imread(file)
            center = pic.shape / 2
            if ((center[0]) < 201 and (center[1] < 201)):
                x = center[1] - w / 2
                y = center[0] - h / 2
                pic = pic[int(y):int(y + h), int(x):int(x + w)]
            else:
                print("jpg is too small to cut")
        except:
            print("Unable to cut jpg", file)
    else:
        print("Unable to cut file", file, "because it is not a jpg")

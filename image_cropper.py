# Merge with attraction picture downloader

import cv2
import glob

print(glob.glob("Attraction Pictures/*"))

w = 400
h = 400
for file in glob.glob("Attraction Pictures/*"):
    if file.endswith('.jpg'):
        try:
            pic = cv2.imread(file)
            height, width, color = pic.shape
            mid_height = int(height / 2)
            mid_width = int(width / 2)
            if ((mid_height > 200) and (mid_width > 200)):
                x = mid_width - w / 2
                y = mid_height - h / 2
                cropped_pic = pic[int(y):int(y + h), int(x):int(x + w)]
                cv2.imwrite(file, cropped_pic)
                print("jpg was cut.")
            else:
                print("jpg is too small to cut.")
        except:
            print("PROBLEM: Unable to cut jpg", file)
    else:
        print("Unable to cut file", file, "because it is not a jpg")
# Merge with attraction picture downloader

import cv2
import glob

# Note: This list needs to be deleted in a bit
unable_to_crop_jpegs_list = []

for file in glob.glob("Attraction Pictures/*"):
    if file.endswith('.jpg'):
        try:
            pic = cv2.imread(file)
            height, width, color = pic.shape
            mid_height = int(height / 2)
            mid_width = int(width / 2)

            # Case 1: length and width are both greater than 400 ---> length and width are both cropped to center 400x400 pixels
            if ((mid_height > 200) and (mid_width > 200)):
                w = 400
                h = 400

                x = mid_width - w / 2
                y = mid_height - h / 2

                cropped_pic = pic[int(y):int(y + h), int(x):int(x + w)]
                cv2.imwrite(file, cropped_pic)
                print(" >400 height by >400 width jpg was cut.")
            # Case 2: height is greater than 400, but width is less than or equal to 400 ---> crop height to size of width
            elif ((mid_height > 200) and (mid_width <= 200)):
                w = width
                h = width

                y = mid_height - h / 2

                cropped_pic = pic[int(y):int(y + h), 0:int(width)]
                cv2.imwrite(file, cropped_pic)
                print(" >400 height by <=400 width jpg was cut.")
            # Case 3: width is greater than 400, but height is less than or equal to 400 ---> crop height to size of height
            elif ((mid_height <= 200) and (mid_width > 200)):
                w = height
                h = height

                x = mid_height - h / 2

                cropped_pic = pic[0:int(height), int(x):int(x + w)]
                cv2.imwrite(file, cropped_pic)
                print(" >400 height by <=400 width jpg was cut.")
            # Case 4: both width and height are less than/equal to 400 ---> crop height or width to the size of the smaller one
            elif ((mid_height <= 200) and (mid_width <= 200)):
                # Case 4A: both height is smaller than width
                if width < height:
                    w = width
                    h = width

                    y = mid_height - h / 2

                    cropped_pic = pic[int(y):int(y + h), 0:int(width)]
                    cv2.imwrite(file, cropped_pic)
                    print("<400 height by <400 width jpg was cut.")
                # Case 4A: both height is smaller than width
                elif height < width:
                    w = height
                    h = height

                    x = mid_height - h / 2

                    cropped_pic = pic[0:int(height), int(x):int(x + w)]
                    cv2.imwrite(file, cropped_pic)
                    print("<400 height by <400 width jpg was cut.")
            else:
                print("jpg is already a square that is 400 by 400 or smaller")
        except:
            print("PROBLEM: UNABLE TO CUT JPEG!!!", file)
            unable_to_crop_jpegs_list.append(file)
    else:
        print("UNABLE TO CUT FILE", file, "because it is not a jpg")
print(unable_to_crop_jpegs_list)
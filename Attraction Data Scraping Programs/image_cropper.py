# Merge with attraction picture downloader

import cv2
import glob

# Loop through every image in Attraction Pictures
for file in glob.glob("Attraction Pictures/*"):

    # Check to make sure that a file is a jpeg
    if file.endswith('.jpg'):

        try:
            # Read image as a matrix of pixels
            pic = cv2.imread(file)

            # Unpack matrix into multiple lists
            height, width, color = pic.shape

            # Take half of height and width to find the center of the image
            mid_height = int(height / 2)
            mid_width = int(width / 2)

            # Case 1: length and width are both greater than 400 ---> length and width are both cropped to center 400x400 pixels
            if ((mid_height > 200) and (mid_width > 200)):

                # Constants needed for cropping
                w = 400
                h = 400
                x = mid_width - w / 2
                y = mid_height - h / 2

                # Cropping picture using list indexing
                cropped_pic = pic[int(y):int(y + h), int(x):int(x + w)]

                # Write in the cropped image over the old image
                cv2.imwrite(file, cropped_pic)

                print(" >400 height by >400 width jpg was cut.")
            # Case 2: height is greater than 400, but width is less than or equal to 400 ---> crop height to size of width
            elif ((mid_height > 200) and (mid_width <= 200)):

                # Constants needed for cropping
                w = width
                h = width
                y = mid_height - h / 2

                # Cropping picture using list indexing
                cropped_pic = pic[int(y):int(y + h), 0:int(width)]

                # Write in the cropped image over the old image
                cv2.imwrite(file, cropped_pic)

                print(" >400 height by <=400 width jpg was cut.")
            # Case 3: width is greater than 400, but height is less than or equal to 400 ---> crop height to size of height
            elif ((mid_height <= 200) and (mid_width > 200)):

                # Constants needed for cropping
                w = height
                h = height
                x = mid_height - h / 2

                # Cropping picture using list indexing
                cropped_pic = pic[0:int(height), int(x):int(x + w)]

                # Write in the cropped image over the old image
                cv2.imwrite(file, cropped_pic)

                print(" >400 height by <=400 width jpg was cut.")
            # Case 4: both width and height are less than/equal to 400 ---> crop height or width to the size of the smaller one
            elif ((mid_height <= 200) and (mid_width <= 200)):

                # Case 4A: width is smaller than height
                if width < height:

                    # Constants needed for cropping
                    w = width
                    h = width
                    y = mid_height - h / 2

                    # Cropping picture using list indexing
                    cropped_pic = pic[int(y):int(y + h), 0:int(width)]

                    # Write in the cropped image over the old image
                    cv2.imwrite(file, cropped_pic)

                    print("<400 height by <400 width jpg was cut.")
                # Case 4B: height is smaller than width
                elif height < width:

                    # Constants needed for cropping
                    w = height
                    h = height
                    x = mid_height - h / 2

                    # Cropping picture using list indexing
                    cropped_pic = pic[0:int(height), int(x):int(x + w)]

                    # Write in the cropped image over the old image
                    cv2.imwrite(file, cropped_pic)

                    print("<400 height by <400 width jpg was cut.")
            # jpeg is already a square of the appropriate size and does not need to be cut more
            else:

                print("jpg is already a square that is 400 by 400 or smaller")
        # jpeg was not cut for some reason and needs to be cut manually
        except:

            print("PROBLEM: UNABLE TO CUT JPEG!!!", file)
    # image is not a jpeg and, thus, can not be cut
    else:

        print("UNABLE TO CUT FILE", file, "because it is not a jpg")
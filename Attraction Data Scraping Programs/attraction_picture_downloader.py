import pandas as pd
import wget
import os
import time as time
import signal
import glob
import shutil


# Import postgreSQL database data
complete_data = pd.read_csv("Application Data and Documentation Files/Attractions Data.csv")

# Import a list of links from the data
links = list(complete_data['image_link_src'].astype("str"))

# Import a list of cities from the data
cities = list(complete_data['city'].astype("str"))

# Create a function that raises an exception
def handler(signum, frame):
    raise Exception('Action took too much time')

# Loop that goes through every city and its corresponding id in the data
for idx, city in enumerate(cities, 1):

    # Function that signals an exception using the handler function
    signal.signal(signal.SIGALRM, handler)

    # Start a 10-second timer
    signal.alarm(10)

    # Try to download the image
    try:

        # Create a name for each image
        file_name = str(idx) + " - " + city + ".jpg"

        # Get the image url
        url = links[idx - 1]

        # Download the url (the name will not be correct)
        old_file_name = wget.download(url)

        # Rename image properly
        os.rename(old_file_name, file_name)
        print(file_name, "downloaded!")

        # Loop that checks the time
        for i in range(0, 5):
            time.sleep(1)

    # Move to this code if the try section takes longer than 10 seconds to execute
    except:

        # Create a name for each file
        file_name = str(idx) + " - " + city + ".txt"

        # Open a file named with the file name made earlier
        open(file_name, 'a').close()

        # Print a message to the console saying that the image could not be downloaded
        print("Unable to download", file_name)

    # End the 10-second timer
    signal.alarm(10)

    # Exit the timer
    signal.alarm(0)

# Create a list of attractions sorted by id
list_of_attraction_pics = sorted(list(glob.glob("*")))[:-25]

# Find the attraction picture folder
attraction_picture_folder = "Attraction Pictures/"

# Loop that goes through each file in the attraction pictures list created earlier
for file in list_of_attraction_pics:

    # Move a file to the attraction picture folder
    shutil.move(file, attraction_picture_folder)
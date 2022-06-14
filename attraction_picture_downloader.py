import pandas as pd
import wget

complete_data = pd.read_csv("more_data.csv")
links = list(complete_data['image_link-src'].astype("str"))[27:]
print(links)
cities = list(complete_data['city'].astype("str"))[27:]


for idx, city in enumerate(cities, 1):
    try:
        file_name = str(idx) + " - " + city + ".jpg"
        url = links[idx - 1]

        old_file_name = wget.download(url)
        #os.rename(old_file_name, file_name)
        print(file_name, "downloaded!")
    except:
        file_name = str(idx) + " - " + city + ".txt"
        open(file_name, 'a').close()
        print("Unable to download", file_name)
import pandas as pd
import wget
import os

complete_data = pd.read_csv("more_data.csv")
links = list(complete_data['image_link-src'].astype("str"))
cities = list(complete_data['city'].astype("str"))

#def downloader(url, file_name):
    #res = requests.get(url, stream=True)
    #if res.status_code == 200:
        #with open(file_name,'wb') as f:
            #shutil.copyfileobj(res.raw, f)
        #print('Image sucessfully Downloaded: ',file_name)
    #else:
        #print('Image Couldn\'t be retrieved')


#def downloader(image_url, file_name):

    #f = open(file_name, 'wb')
    #f.write(shutil.copyfileobj(res.raw, f))
    #f.close()


for idx, city in enumerate(cities, 1):
    try:
        file_name = str(idx) + " - " + city + ".jpg"
        url = links[idx - 1]

        old_file_name = wget.download(url)
        os.rename(old_file_name, file_name)
        print(file_name, "downloaded!")
    except:
        file_name = str(idx) + " - " + city + ".txt"
        open(file_name, 'a').close()
        print("Unable to download", file_name)
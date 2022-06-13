# Ideas for Scraping Websites for Data
# - Id column is ok.
# - Name: Thomas's Extension.
# - Description: Use Meta code. Thomas's Extension as a backup.
# - State column is ok.
# - City column is ok.
# - Type: Filler Value. NEEDS EDITING LATER!!!
# - Price_level: Filler Value. NEEDS EDITING LATER!!!
# - Traffic_level: Filler Value. NEEDS EDITING LATER!!!
# - Rating: Thomas's Extension.
# - Wheelchair_accessibility: Thomas's Extension.
# - Family_friendly: Thomas's Extension.
# - Pet_friendly: Filler Value. NEEDS EDITING LATER!!!
# - Website: Thomas's Extension.
# - Lat: Use Geopy Code.
# - Long: Use Geopy Code.
# - Image column: Thomas's Extension.

import pandas as pd
from bs4 import BeautifulSoup
from geopy import geocoders
import glob
import requests

all_data = pd.DataFrame()
for file in glob.glob("rawcsv/*"):
    city_data = pd.read_csv(file)
    all_data = all_data.append(city_data)
    print("Checkpoint 1: City Added")
print("Checkpoint 2 (Number of Cities Total):", len(all_data))

def combiner(df):
    odds = list(range(1, len(df) + 1, 2))
    evens = list(range(2, len(df) + 1, 2))
    combined_all_data = pd.DataFrame()
    for number in range(0,len(evens)):
        odd_number = odds[number]
        even_number = evens[number]
        combined_datapoint = df.iloc[odd_number-1].combine_first(df.iloc[even_number-1])
        combined_all_data = combined_all_data.append(combined_datapoint)
    print("Checkpoint 4:", combined_all_data)
    return combined_all_data


all_data = all_data.groupby('web-scraper-start-url')[['name', 'rating', 'website', 'location', 'wheelchair', 'family', 'image_link-src', 'description']].first()
print("Checkpoint 3:", all_data)

combined_all_data = combiner(all_data)

description_list = []
for url in combined_all_data['website']:
    if bool(url):
        try:
            page = requests.get('https://' + url)
            soup = BeautifulSoup(page.content, "html.parser")
            metas = soup.find_all('meta')
            description = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
            description_list.append(''.join(description))
            print("Checkpoint 5:", description_list)
        except:
            try:
                page = requests.get('http://' + url)
                soup = BeautifulSoup(page.content, "html.parser")
                metas = soup.find_all('meta')
                description = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
                description_list.append(''.join(description))
                print("Checkpoint 5:", description_list)
            except:
                description_list.append(None)
                print("Checkpoint 5:", description_list)
    else:
        description_list.append(None)
        print("Checkpoint 5:", description_list)

print("Checkpoint 6 (Full Description List Length):", len(description_list))

locator = geocoders.GoogleV3(api_key="AIzaSyDUWchqTkzvxteGNb_tDPCR3jvL1k5J_g4", user_agent="scraping_test.ipynb")
latitude_list = []
longitude_list = []
for location in combined_all_data['location']:
    try:
        coordinates = locator.geocode(location)
        latitude = coordinates.latitude
        longitude = coordinates.longitude
        latitude_list.append(latitude)
        longitude_list.append(longitude)
        print("Checkpoint 7:", latitude_list)
    except:
        latitude_list.append(None)
        longitude_list.append(None)
        print("Checkpoint 7:", latitude_list)

combined_all_data['meta_descriptions'] = description_list
combined_all_data['latitude'] = latitude_list
combined_all_data['longitude'] = longitude_list
combined_all_data = combined_all_data.reset_index(drop = True)

print("Checkpoint 8 (Final Dataframe created)")

combined_all_data.to_csv('complete_data.csv')
print("Checkpoint 9 (Process Complete)")
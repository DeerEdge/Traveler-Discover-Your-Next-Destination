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
for file in glob.glob("rawCSV/*"):
    city_data = pd.read_csv(file)
    all_data = all_data.append(city_data)

for id, element in enumerate(all_data['web-scraper-order']):
    element = element[-3:]
    all_data['web-scraper-order'][id] = element

def combiner(df):
    odds = list(range(1, len(df) + 1, 2))
    evens = list(range(2, len(df) + 1, 2))
    combined_all_data = pd.DataFrame()
    for number in range(0,len(evens)):
        odd_number = odds[number]
        even_number = evens[number]
        combined_datapoint = df.iloc[odd_number-1].combine_first(df.iloc[even_number-1])
        combined_all_data = combined_all_data.append(combined_datapoint)
    return combined_all_data


all_data = all_data.groupby('web-scraper-start-url')[['name', 'rating', 'website', 'location', 'wheelchair', 'family', 'image_link-src', 'description']].first()
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
        except:
            try:
                page = requests.get('http://' + url)
                soup = BeautifulSoup(page.content, "html.parser")
                metas = soup.find_all('meta')
                description = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and meta.attrs['name'] == 'description' ]
                description_list.append(''.join(description))
            except:
                description_list.append(None)
    else:
        description_list.append(None)

locator = geocoders.GoogleV3(api_key="AIzaSyDUWchqTkzvxteGNb_tDPCR3jvL1k5J_g4", user_agent="scraping_test.ipynb")
latitude_list = []
longitude_list = []
for location in combined_all_data['location']:
    coordinates = locator.geocode(location)
    latitude = coordinates.latitude
    longitude = coordinates.longitude
    latitude_list.append(latitude)
    longitude_list.append(longitude)

combined_all_data['meta_descriptions'] = description_list
combined_all_data['latitude'] = latitude_list
combined_all_data['longitude'] = longitude_list
combined_all_data = combined_all_data.reset_index(drop = True)

combined_all_data.to_csv('complete_data.csv')
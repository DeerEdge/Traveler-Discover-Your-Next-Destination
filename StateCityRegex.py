import pandas as pd
import regex as re

complete_data = pd.read_csv("complete_data.csv")

def getState(address):
    return address[-8:-6]

def getCity(address):
    city = re.search("(?<=.*,\s).*(?=,\s[A-Z]{2}\s[0-9]{5})",address)
    if city:
        return city.group()
    else:
        return city

complete_data = complete_data['location'].astype("str")

state_city_dataframe = pd.DataFrame([complete_data.apply(getState),complete_data.apply(getCity)], index = ['State', 'City'])

state_city_dataframe.to_csv('state_city_data.csv')
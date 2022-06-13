import pandas as pd
import regex as re

# Merge this with "Scraping.py"
complete_data = pd.read_csv("final_data.csv")


def getState(address):
    return address[-8:-6]


def getCity(address):
    city = re.search("(?<=.*,\s).*(?=,\s[A-Z]{2}\s[0-9]{5})", address)
    if city:
        return city.group()
    else:
        return city


complete_data = complete_data['location'].astype("str")


states = complete_data.apply(getState)
states_dict = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado",
               "CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho",
               "IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine",
               "MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri",
               "MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico",
               "NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon",
               "PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee",
               "TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia",
               "WI":"Wisconsin","WY":"Wyoming"}

cities = complete_data.apply(getCity)


state_city_dataframe = pd.DataFrame(list(zip(states, cities)), columns=['State', 'City'])
state_city_dataframe['State'] = state_city_dataframe['State'].map(states_dict)

state_city_dataframe.to_csv('state_city_data.csv')
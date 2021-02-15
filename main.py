"""Main module for films map creation"""
import pandas as pd
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim
from map_creation import main as create_map

year = int(input('Please enter a year you would like to have a map for: '))
coordinates = tuple(
    map(float, input('Please enter your location (format: lat long): ').split(' ')))
print('Locations are getting collected...')

locator = Nominatim(user_agent='dyaroshevych111')
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

USER_COUNTRY = locator.reverse(coordinates, language='en')[-2].split(", ")[-1]

if USER_COUNTRY == 'United States':
    USER_COUNTRY = 'USA'

df = pd.read_csv('locations.csv')
df = df[df['Country'] == USER_COUNTRY]


print('Map is generating...')
create_map(df, coordinates, geocode)
print('Finished. Please have look at the map films_map.html')

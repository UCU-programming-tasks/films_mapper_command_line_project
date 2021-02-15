import pandas as pd
from map_creation import main as create_map
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

year = int(input('Please enter a year you would like to have a map for: '))
coordinates = tuple(
    map(float, input('Please enter your location (format: lat long): ').split(' ')))
print('Locations are getting collected...')

locator = Nominatim(user_agent='dyaroshevych111')
geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

country = locator.reverse(coordinates, language='en')[-2].split(", ")[-1]

if country == 'United States':
    country = 'USA'

df = pd.read_csv('locations.csv')
df = df[df['Country'] == country]


print('Map is generating...')
create_map(df, coordinates, geocode)
print('Finished. Please have look at the map films_map.html')

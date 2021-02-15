"""Module for creating a map with markers for films near the user location."""
from typing import List, Tuple
import pandas as pd
import folium
import haversine
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderUnavailable
from folium.plugins import MarkerCluster


def init(user_agent: str = 'dyaroshevych') -> RateLimiter:
    """
    Initialize locator and geocode.
    """
    locator = Nominatim(user_agent=user_agent)
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

    return geocode


def geocode_with_exception(loc, geocode):
    """
    Find location. If no location can be found, return None.
    """
    try:
        return geocode(loc)
    except GeocoderUnavailable:
        return None


def add_coordinates(df: pd.DataFrame, coordinates: List[float],
                    num_places: int, geocode) -> pd.DataFrame:
    """
    Add coordinates information to a slice of the given DataFrame.
    """
    df_small = df.head(num_places)

    locations = df_small['Location'].apply(
        lambda loc: geocode_with_exception(loc, geocode))
    df_small.dropna(how='any', inplace=True)
    df_small['Point'] = locations.apply(
        lambda loc: tuple(loc.point) if loc else None)
    df_small[['Latitude', 'Longitude', 'Altitude']] = pd.DataFrame(
        df_small['Point'].tolist(), index=df_small.index)

    df_small.drop(columns=['Point', 'Altitude'], inplace=True)
    df_small.dropna(how='any', inplace=True)

    df_small['Distance'] = df_small[['Latitude', 'Longitude']].apply(
        lambda coords: get_distance(list(coords), coordinates), axis=1)

    df_small.sort_values(by='Distance', inplace=True)

    return df_small.head(10)


def get_distance(coords_1: List[float], coords_2: List[float]) -> float:
    """
    Calculate distance between two points with given coordinates.
    """
    return haversine.haversine(coords_1, coords_2)


def create_map(coordinates: Tuple[float, float], data: pd.DataFrame) -> folium.Map:
    """
    Create a map with all given locations.
    """
    films_map = folium.Map(
        location=coordinates,
        zoom_start=8,
    )

    films_map.add_child(folium.Marker(
        coordinates, popup='You', icon=folium.Icon(color='red', icon='home', prefix='fa')))

    marker_cluster = MarkerCluster().add_to(films_map)
    locations = list(zip(data['Latitude'].values, data['Longitude'].values))

    for idx, location in enumerate(locations):
        popup = folium.Popup(data['Title'].iloc[idx])

        folium.Marker(location, popup=popup).add_to(marker_cluster)

    folium.LayerControl().add_to(films_map)

    return films_map


def main(df: pd.DataFrame, coordinates: Tuple[float, float], geocode: RateLimiter,
         num_places: int = 60, output_filename: str = 'films_map.html'):
    """
    Get information about locations from the DataFrame and save them as an html map.
    """
    small_df = add_coordinates(df, coordinates, num_places, geocode)
    films_map = create_map(coordinates, small_df)

    films_map.save(output_filename)

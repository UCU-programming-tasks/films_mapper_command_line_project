"""Functions for transforming raw data about the films into csv"""

from typing import List, Tuple
import pandas as pd


def extract_info(line: str):
    """
    Extract information from raw string with information
    about the film: title, year and location. If data is
    invalid, return None.
    """
    try:
        # Extract title which is either surrounded with "" or not
        if line[0] == '"':
            line = line[1:]
            title = line[:line.find('"')]
        else:
            title = line[:line.find(' ')]

        # Extract year which is located inside parentheses
        year_start_idx = line.find('(')
        year = int(line[year_start_idx + 1:year_start_idx + 5])

        # Extract location from the
        if '\t\t' not in line:
            location = line.rsplit('}\t', maxsplit=1)[1]
        else:
            location = line.rsplit('\t\t', maxsplit=1)[1]

        # Clear up the location
        location = location.rsplit(
            '(', maxsplit=1)[0].replace('\t', '').rsplit('\n')[0]

        return title, year, location
    except Exception:
        # If an error occurs, raw data is invalid
        return None


def read_data(filename: str) -> List[Tuple[str, int, str]]:
    """
    Read data about films from the given file and transform it into a list.
    """
    with open(filename, 'r', errors='ignore') as locations_raw:
        lines = locations_raw.readlines()

    locations = []

    for line in lines:
        data = extract_info(line)

        if data is None:
            continue

        locations.append(data)

    return locations


def save_data(data: pd.DataFrame, filename: str):
    """
    Save the data into a given file.
    """
    data.to_csv(filename, index=False)


def transform_data(data: List[Tuple[str, int, str]]) -> pd.DataFrame:
    """
    Transform the given data into a DataFrame. Data is expected to
    contain information about film titles, years and locations.
    """
    df = pd.DataFrame(data, columns=['Title', 'Year', 'Location'])

    # Add a column with country name
    df['Country'] = df['Location'].str.rsplit(', ').apply(lambda x: x[-1])

    # Remove rows where location is equal to country name
    df = df[~(df['Country'] == df['Location'])]

    # Drop rows with duplicated location
    df.drop_duplicates(subset='Location', keep='first', inplace=True)

    return df


def main(filename: str, output_filename: str = 'locations.csv'):
    """
    Read raw data from the file, transform it into DataFrame and save.
    The default output filename is 'locations.csv'.
    """
    data = read_data(filename)
    df = transform_data(data)
    save_data(df, output_filename)


main('locations.list')

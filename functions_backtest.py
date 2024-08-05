from bs4 import BeautifulSoup
import geopandas as gpd
from shapely.geometry import Point

from shapely.geometry import MultiPolygon
import pandas as pd 
from shapely.geometry import Polygon

def kml_to_geojson(chemin_kml):
    levels = {
        "<5%": 1,
        "5-10": 2,
        "10-20": 3,
        "20-30": 4,
        "30-40": 5,
        "40-50": 6,
        "50-60": 7,
        "60-70": 8,
        "70-80": 9,
        "80-90": 10,
        ">90%": 11
    }

    # Read the KML file and parse it with BeautifulSoup
    with open(chemin_kml, "r",, encoding="utf-8") as f:
        kml_data = f.read()

    soup = BeautifulSoup(kml_data, "xml")

    # Create a GeoDataFrame to store the features
    gdf = gpd.GeoDataFrame(columns=['Name', 'Geometry'])

    # Extract data from Placemark elements
    for placemark in soup.find_all("Placemark"):
        name = placemark.find("name").text.strip()
        for polygon in placemark.find_all("Polygon"):
            coordinates_str = polygon.find("coordinates").text.strip()

            # Split the coordinates into latitude and longitude pairs
            coordinates = [tuple(map(float, coord.split(","))) for coord in coordinates_str.split()]

            # Create a Polygon geometry
            polygon = Polygon(coordinates)

            # Append the data to the GeoDataFrame
            gdf.loc[len(gdf)] = {'Name': name, 'Geometry': polygon}

    gdf["level"] = gdf["Name"].apply(lambda x: levels[x])
    gdf = gdf.sort_values(by="level")
    # Return the GeoDataFrame
    return gdf


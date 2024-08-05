from bs4 import BeautifulSoup
import geopandas as gpd
from shapely.geometry import MultiPolygon,Point,Polygon
import pandas as pd 

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
    with open(chemin_kml, "r", encoding="utf-8") as f:
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

def points_in_polygons_(df_points, gdf):
    # Vérifier si les points sont à l'intérieur des polygones
    points_in_polygons = []
    geometry_points = [Point(xy) for xy in zip(df_points['LON'], df_points['LAT'])]
    gdf_points = gpd.GeoDataFrame(df_points, geometry=geometry_points)
    for point in gdf_points.iterrows():
        for poly in gdf.iterrows():
            if point[1]['geometry'].within(poly[1]['Geometry']):
                point_data = point[1].copy()  # Copier les données du point
                point_data['POLYGON_AREA'] = poly[1]['Name']  # Ajouter la valeur 'Name' du polygone
                point_data['LEVEL']=poly[1]['level']
                points_in_polygons.append(point_data)

    result_df = gpd.GeoDataFrame(points_in_polygons)
    
    # Créer un DataFrame à partir des points à l'intérieur des polygones
    result_df = result_df.sort_values(by='LEVEL', ascending=False)
    # Supprimer les doublons en se basant sur les colonnes spécifiées
    result_df = result_df.drop_duplicates(subset=['LOCATION', 'ENTITY', 'CITY', 'COUNTRY', 'LAT', 'LON', 'TIV'])
    
    result_df = result_df.drop(columns=['geometry','LEVEL'])
    return result_df

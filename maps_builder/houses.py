import osmnx as ox
import geopandas as gpd
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Example CLI parser")
parser.add_argument("--osm", required=True, help="The path to an OSM XML file")
args = parser.parse_args()
FILE_NAME = args.osm

tags = {"addr:housenumber": True, "addr:street": True, "building": True}
houses = ox.features_from_xml(FILE_NAME, tags=tags)
houses = houses[['addr:housenumber', 'addr:street', 'geometry']]
houses = houses.dropna(subset=['addr:housenumber', 'addr:street'])
houses['addr:street'] = houses['addr:street'].apply(lambda x: str(x).strip())

def parse_numbers(n):
    try:
        if '-' in str(n):
            return [int(x) for x in str(n).split('-')]
        else:
            return [int(n)]
    except:
        return []

houses['numbers'] = houses['addr:housenumber'].apply(parse_numbers)
houses = houses.explode('numbers')
houses = houses.rename(columns={'numbers': 'housenumber'})
houses = houses[houses['housenumber'].notna()]
houses = houses[houses['housenumber'] != '']

houses = houses.to_crs(epsg=3857)
houses['geometry'] = houses.geometry.centroid
houses = houses.to_crs(epsg=4326)
houses['lat'] = houses.geometry.y
houses['lon'] = houses.geometry.x

houses[['addr:street', 'housenumber', 'lat', 'lon']].to_csv(f"{FILE_NAME.replace('.osm', '')}_houses.csv", 
    header=False,index=False)
print("✅ Extracted", len(houses), "house numbers with coordinates")

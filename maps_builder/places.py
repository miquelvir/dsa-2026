import osmnx as ox
import geopandas as gpd
import pandas as pd
import argparse
import uuid

parser = argparse.ArgumentParser(description="Extract places of interest from an OSM XML file")
parser.add_argument("--osm", required=True, help="The path to an OSM XML file")
args = parser.parse_args()
FILE_NAME = args.osm

tags = {
    "amenity": True,
    "shop": True,
    "office": True,
    "tourism": True,
    "leisure": True,
    "craft": True,
    "name": True
}

pois = ox.features_from_xml(FILE_NAME, tags=tags)
columns = [col for col in ["name", "amenity", "shop", "office", "tourism", "leisure", "craft", "geometry"] if col in pois.columns]
pois = pois[columns].dropna(subset=["geometry"])

pois = pois.to_crs(epsg=3857)
pois["geometry"] = pois.geometry.centroid
pois = pois.to_crs(epsg=4326)
pois["lat"] = pois.geometry.y
pois["lon"] = pois.geometry.x

def get_category(row):
    for key in ["amenity", "shop", "office", "tourism", "leisure", "craft"]:
        if key in row and pd.notna(row[key]):
            return f"{key}:{row[key]}"
    return "other"
pois["category"] = pois.apply(get_category, axis=1)

pois = pois[pois['name'].notna()]
pois = pois[pois['name'] != '']
pois = pois[pois['category'] != 'other']
pois["name"] = pois["name"].astype(str).str.replace(", ", " ", regex=False).replace(",", " ", regex=False).str.strip()

pois["uuid"] = [str(uuid.uuid4()) for _ in range(len(pois))]

pois_out = pois[["name", "category", "lat", "lon"]].fillna("")
output_csv = f"{FILE_NAME.replace('.osm', '')}_pois.txt"
pois_out.to_csv(output_csv, index=False, header=False)

print(f"✅ Extracted {len(pois_out)} places of interest to {output_csv}")

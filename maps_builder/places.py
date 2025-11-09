import osmnx as ox
import geopandas as gpd
import pandas as pd
import argparse
import uuid

parser = argparse.ArgumentParser(description="Extract places of interest from an OSM XML file")
parser.add_argument("--osm", required=True, help="The path to an OSM XML file")
args = parser.parse_args()
FILE_NAME = args.osm

import osmium
import pandas as pd
import uuid

allowed_tags = ["amenity", "shop", "office", "tourism", "leisure", "craft"]

class POIHandler(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.pois = []

    def node(self, n):
        if not n.tags:
            return
        name = n.tags.get("name")
        if not name:
            return
        for tag in allowed_tags:
            if tag in n.tags:
                self.pois.append({
                    "uuid": str(uuid.uuid4()),
                    "name": name.strip().replace(", ", " ").replace(",", " "),
                    "category": f"{tag}:{n.tags[tag]}",
                    "lat": n.location.lat,
                    "lon": n.location.lon,
                    "uuid": str(uuid.uuid4()),
                })
                break

h = POIHandler()
h.apply_file(FILE_NAME, locations=True)

pois_df = pd.DataFrame(h.pois)
pois_df.to_csv(FILE_NAME.replace(".osm", "")+"_places.csv", index=False, header=False, columns=["uuid", "name","category","lat","lon"])
print(f"✅ Extracted {len(pois_df)} POIs")

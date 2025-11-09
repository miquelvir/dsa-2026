import osmium
import pandas as pd
import argparse
import re

parser = argparse.ArgumentParser(description="Extract building addresses from an OSM XML/PBF file")
parser.add_argument("--osm", required=True, help="The path to an OSM or PBF file")
args = parser.parse_args()
FILE_NAME = args.osm

class AddressExtractor(osmium.SimpleHandler):
    def __init__(self):
        super().__init__()
        self.rows = []

    def node(self, n):
        tags = n.tags
        if 'addr:housenumber' in tags and 'addr:street' in tags:
            lat = n.location.lat
            lon = n.location.lon
            self.add_entry(tags['addr:street'], tags['addr:housenumber'], lat, lon)

    def way(self, w):
        tags = w.tags
        if 'addr:housenumber' in tags and 'addr:street' in tags and w.nodes:
            # Compute centroid of way geometry (approximate average)
            lats = [n.lat for n in w.nodes if n.location.valid()]
            lons = [n.lon for n in w.nodes if n.location.valid()]
            if not lats or not lons:
                return
            lat = sum(lats) / len(lats)
            lon = sum(lons) / len(lons)
            self.add_entry(tags['addr:street'], tags['addr:housenumber'], lat, lon)

    def add_entry(self, street, housenumber, lat, lon):
        housenumber = str(housenumber).strip()
        street = str(street).strip()
        if not housenumber or not street:
            return

        match = re.match(r'(\d+)', housenumber)
        if match:
            number_only = int(match.group(1))
            self.rows.append((street, number_only, lat, lon))
        else:
            print(f"Skipping malformed line: {street},{housenumber},{lat},{lon}")



handler = AddressExtractor()
handler.apply_file(FILE_NAME, locations=True)

houses_df = pd.DataFrame(handler.rows, columns=["street", "housenumber", "lat", "lon"])

output_csv = f"{FILE_NAME.replace('.osm', '')}_houses.csv"
houses_df.to_csv(output_csv, header=False, index=False)

print(f"✅ Extracted {len(houses_df)} house numbers with coordinates to {output_csv}")

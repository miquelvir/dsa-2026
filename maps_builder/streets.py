import osmnx as ox
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Example CLI parser")
parser.add_argument("--osm", required=True, help="The path to an OSM XML file")
args = parser.parse_args()
FILE_NAME = args.osm

G = ox.graph_from_xml(FILE_NAME, simplify=True)

edges = ox.graph_to_gdfs(G, nodes=False, edges=True).reset_index()
cols = [c for c in ['u','v','length','name','highway'] if c in edges.columns]
edges_df = edges[cols].copy()

def normalize_name(x):
    if isinstance(x, list):
        return x[0]
    return x

def normalize_highway(x):
    if isinstance(x, list):
        return x[0]
    return x

edges_df['name'] = edges_df['name'].apply(normalize_name)
edges_df['highway'] = edges_df['highway'].apply(normalize_highway)
allowed_highways = ['motorway','trunk','primary','secondary','tertiary','residential','unclassified']
edges_df = edges_df[edges_df['highway'].isin(allowed_highways)]

nodes = pd.DataFrame.from_dict({n: (data['y'], data['x']) for n, data in G.nodes(data=True)}, orient='index', columns=['lat','lon'])
edges_df = edges_df.merge(nodes, left_on='u', right_index=True, how='left')
edges_df = edges_df.rename(columns={'lat':'lat_u','lon':'lon_u'})
edges_df = edges_df.merge(nodes, left_on='v', right_index=True, how='left')
edges_df = edges_df.rename(columns={'lat':'lat_v','lon':'lon_v'})
edges_df.to_csv(f"{FILE_NAME.replace('.osm', '')}_streets.csv", index=False,
    header=False, columns=[
    'u', 'lat_u', 'lon_u', 'v', 'lat_v', 'lon_v', 'length', 'name'
])
print("✅ Exported", len(edges_df), "edges with coordinates")
print(edges_df.head())

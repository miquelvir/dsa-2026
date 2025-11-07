# Creating custom maps

You can build your own maps if you want:

1. Navigate to a region in [OpenStreetMap](https://www.openstreetmap.org/export#map=16/41.39706/2.15935).
2. Click `Overpass API` to download an XML file with all the map data. Copy the path to this file.
3. Create the `houses.txt` and `streets.txt` files:

```zsh
cd maps_builder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 houses.py --osm path_to_downloaded_file
python3 streets.py --osm path_to_downloaded_file
python3 places.py --osm path_to_downloaded_file
```

# backend/download_map.py
import osmnx as ox
import time

ox.settings.overpass_max_area = 100_000_000  # increase allowed query area


print(f"--- Using OSMnx version: {ox.__version__} ---")

# Allow large query areas
ox.settings.overpass_max_area = 10_000_000

# Define bounding box
north, south, east, west = 23.2415, 23.2405, 72.5045, 72.5035
bbox = (north, south, east, west)

print("--- Starting map download... ---")
start_time = time.time()

try:
    from osmnx import graph, save_graphml

    # ✅ OSMnx 2.x requires bbox=(north, south, east, west)
    G = graph.graph_from_bbox(bbox=bbox, network_type="drive")

    save_graphml(G, filepath="map.graphml")

    end_time = time.time()
    print(f"--- SUCCESS: Map data saved as map.graphml in {end_time - start_time:.2f} seconds. ---")

except Exception as e:
    print(f"❌ ERROR: {e}")


# backend/app.py --- FINAL PHASE 3 (STABLE FIXED) ---

from flask import Flask, jsonify, request
from flask_cors import CORS
import osmnx as ox
import requests
import numpy as np
import math
from shapely.geometry import Point

# --- CONFIGURATION ---
app = Flask(__name__)
# Allow only frontend connection to avoid CORS issues
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

WEATHER_API_KEY = "409109e68b27284b3352231c849b2b9e"

# Small bounding box
north, south, east, west = 23.2415, 23.2405, 72.5045, 72.5035
LAT, LON = 23.241, 72.504

# --- SIMULATION PARAMETERS ---
EMISSION_FACTORS = {'car': 120.0}
TRAFFIC_DENSITY = {
    'primary': {'car': 1500},
    'secondary': {'car': 800},
    'residential': {'car': 200},
    'default': {'car': 500}
}
GRID_RESOLUTION = 50

# --- INTERVENTION PARAMETERS ---
VERTICAL_GARDEN_CAPTURE_RATE = 0.5  # g/s
VERTICAL_GARDEN_RADIUS = 30  # meters

# --- HELPER FUNCTIONS ---
def get_weather_data(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        wind_speed = data['wind'].get('speed', 1.0)
        wind_deg = data['wind'].get('deg', 45.0)
        print(f"--- SUCCESS: Weather fetched! Wind={wind_speed} m/s @ {wind_deg}° ---")
        return max(wind_speed, 0.1), wind_deg
    except Exception as e:
        print(f"--- ERROR: Could not fetch weather data: {e} ---")
        return 1.0, 45.0

def gaussian_plume_model(Q, u, x, y, z=1.5):
    sigma_y = 0.22 * x / (1 + 0.0004 * x)**0.5
    sigma_z = 0.20 * x
    if sigma_y == 0 or sigma_z == 0:
        return 0.0
    term1 = Q / (2 * math.pi * u * sigma_y * sigma_z)
    term2 = math.exp(-0.5 * (y / sigma_y)**2)
    term3 = math.exp(-0.5 * (z / sigma_z)**2)
    return term1 * term2 * term3


# --- MAIN SIMULATION ENDPOINT ---
@app.route('/api/simulate', methods=['POST'])
def run_simulation():
    interventions = request.json.get('interventions', [])
    print(f"Received simulation request with {len(interventions)} interventions.")

    # --- Weather ---
    wind_speed_ms, wind_deg = get_weather_data(WEATHER_API_KEY, LAT, LON)
    wind_rad = math.radians(wind_deg)

    # --- Load Map ---
    try:
        G = ox.load_graphml("map.graphml")
        G_proj = ox.project_graph(G)
    except Exception as e:
        print(f"--- ERROR: Could not load map.graphml: {e} ---")
        return jsonify({"error": "Map not found or unreadable"}), 500

    edges = ox.graph_to_gdfs(G_proj, nodes=False, edges=True)

    # --- Source Emission Calculation ---
    sources = []
    for _, edge in edges.iterrows():
        highway_type = edge.get('highway', 'default')
        if isinstance(highway_type, list):
            highway_type = highway_type[0]
        traffic = TRAFFIC_DENSITY.get(highway_type, TRAFFIC_DENSITY['default'])
        length_km = edge['length'] / 1000.0
        emissions_g_hr = traffic['car'] * EMISSION_FACTORS['car'] * length_km
        Q = emissions_g_hr / 3600.0
        centroid = edge.geometry.centroid
        sources.append({'Q': Q, 'x': centroid.x, 'y': centroid.y})

    # --- Grid Setup ---
    gdf_nodes = ox.graph_to_gdfs(G_proj, edges=False)
    min_x, min_y, max_x, max_y = gdf_nodes.total_bounds
    x_coords = np.linspace(min_x, max_x, GRID_RESOLUTION)
    y_coords = np.linspace(min_y, max_y, GRID_RESOLUTION)
    grid_x, grid_y = np.meshgrid(x_coords, y_coords)
    concentration_grid = np.zeros_like(grid_x)

    # --- Dispersion Simulation ---
    for source in sources:
        dx, dy = grid_x - source['x'], grid_y - source['y']
        rotated_x = dx * math.cos(wind_rad) - dy * math.sin(wind_rad)
        rotated_y = dx * math.sin(wind_rad) + dy * math.cos(wind_rad)
        downwind_mask = rotated_x > 0
        conc = np.zeros_like(rotated_x)
        if np.any(downwind_mask):
            conc[downwind_mask] = gaussian_plume_model(source['Q'], wind_speed_ms, rotated_x[downwind_mask], rotated_y[downwind_mask])
        concentration_grid += conc

    # --- Apply Interventions ---
    if interventions:
        print(f"Applying {len(interventions)} vertical garden interventions...")
        for p in interventions:
            point_geom = Point(p['lng'], p['lat'])
            projected_geom = ox.project_geometry(point_geom, to_crs=G_proj.graph['crs'])[0]
            ix, iy = projected_geom.x, projected_geom.y
            distance = np.sqrt((grid_x - ix)**2 + (grid_y - iy)**2)
            mask = distance <= VERTICAL_GARDEN_RADIUS
            concentration_grid[mask] = np.maximum(0, concentration_grid[mask] - VERTICAL_GARDEN_CAPTURE_RATE)

    # --- Normalize Results ---
    max_conc = np.max(concentration_grid)
    if max_conc == 0:
        max_conc = 1.0
    normalized_grid = concentration_grid / max_conc

    # --- Prepare Geo Results ---
    results = []
    for i in range(GRID_RESOLUTION):
        for j in range(GRID_RESOLUTION):
            point_proj = Point(grid_x[i, j], grid_y[i, j])
            point_latlon = ox.project_geometry(point_proj, to_crs="EPSG:4326")[0]
            lon, lat = point_latlon.x, point_latlon.y
            results.append([lon, lat, normalized_grid[i, j]])

    print("--- ✅ SUCCESS: Simulation complete. Sending data to frontend. ---")
    return jsonify(results)


# --- ENTRY POINT ---
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

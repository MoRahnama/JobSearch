import requests
import json
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import cKDTree

# Constants
COLLISION_DATA_URL = 'https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/KSI/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'
TORONTO_OPEN_DATA_API = "https://ckan0.cf.opendata.inter.prod-toronto.ca"
TRAFFIC_SIGNALS_PACKAGE_ID = "traffic-signals-tabular"

def fetch_collision_data(url):
    """
    Fetch traffic collision data from the provided URL and return as a GeoDataFrame.
    """
    response = requests.get(url)
    gdf = gpd.read_file(response.text)
    return gdf

def extract_lat_lon(gdf):
    """
    Extract latitude and longitude coordinates from a GeoDataFrame and add them as new columns.
    """
    gdf['latitude'] = gdf['geometry'].apply(lambda x: x.centroid.y)
    gdf['longitude'] = gdf['geometry'].apply(lambda x: x.centroid.x)
    return gdf

def fetch_package_data(base_url, package_id):
    """
    Fetch package data from CKAN API using package id.
    """
    url = base_url + "/api/3/action/package_show"
    params = {"id": package_id}

    package = requests.get(url, params=params).json()
    return package

def fetch_traffic_signals_data(base_url, package):
    """
    Fetch traffic signals data from CKAN API using package data.
    """
    for resource in package["result"]["resources"]:
        if resource["datastore_active"]:
            url = base_url + "/datastore/dump/" + resource["id"]
            traffic_signals = pd.read_csv(url)
            break
    return traffic_signals

def process_traffic_signals_data(traffic_signals):
    """
    Process traffic signals data and extract latitude and longitude from geometry.
    """
    traffic_signals['geometry'] = traffic_signals['geometry'].apply(lambda x: json.loads(x))
    traffic_signals['LATITUDE'] = traffic_signals['geometry'].apply(lambda x: x['coordinates'][1])
    traffic_signals['LONGITUDE'] = traffic_signals['geometry'].apply(lambda x: x['coordinates'][0])
    return traffic_signals

def calculate_distance_to_nearest_signal(gdf, traffic_signals):
    """
    Calculate the distance from each traffic collision event to the nearest traffic signal.
    """
    tree = cKDTree(traffic_signals[['LATITUDE', 'LONGITUDE']])
    distances, _ = tree.query(gdf[['latitude', 'longitude']].values, k=1)
    gdf['DIST_TO_TRAFFIC_SIGNAL'] = distances
    return gdf

def plot_collision_density_map(gdf):
    """
    Plot a density map of traffic collisions.
    """
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_aspect('equal')
    base = gdf.plot(ax=ax, alpha=0.5, color='red')
    contextily.add_basemap(ax, crs=gdf.crs.to_string(), zoom=12)
    ax.set_title('Density Map of Traffic Collisions Resulting in Fatalities or Serious Injuries in Toronto (2006-2021)')
    plt.show()


def plot_collision_histogram(gdf):
    """
    Plot a histogram of the distances between collisions and the nearest traffic signal.
    """
    distances = pd.Series(gdf['DIST_TO_TRAFFIC_SIGNAL']) * 1000
    sns.histplot(distances, bins=50)
    plt.xlabel('Distance to nearest traffic signal (meters)')
    plt.ylabel('Number of collisions')
    plt.title('Distribution of collision distances to nearest traffic signal')
    plt.show()

def main():
    # Fetch and process traffic collision data
    gdf = fetch_collision_data(COLLISION_DATA_URL)
    gdf = extract_lat_lon(gdf)

    # Fetch and process traffic signals data
    package_data = fetch_package_data(TORONTO_OPEN_DATA_API, TRAFFIC_SIGNALS_PACKAGE_ID)
    traffic_signals = fetch_traffic_signals_data(TORONTO_OPEN_DATA_API, package_data)
    traffic_signals = process_traffic_signals_data(traffic_signals)

    # Calculate the distance from each traffic collision event to the nearest traffic signal
    gdf = calculate_distance_to_nearest_signal(gdf, traffic_signals)

    # Visualize the data
    plot_collision_density_map(gdf)
    plot_collision_histogram(gdf)

if __name__ == "__main__":
    main()


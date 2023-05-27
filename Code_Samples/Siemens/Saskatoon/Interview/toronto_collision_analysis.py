import requests
import json
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily
import folium
from folium.plugins import HeatMap
import pydeck as pdk
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde
from scipy.spatial.distance import pdist, squareform
from scipy.spatial import cKDTree

# Define the URL for the API
url = 'https://services.arcgis.com/S9th0jAJ7bqgIRjw/arcgis/rest/services/KSI/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson'

# Make a GET request to the API
response = requests.get(url)

# Convert the response to a geopandas GeoDataFrame
gdf = gpd.read_file(response.text)

# Extract the latitude and longitude coordinates of each collision event
gdf['latitude'] = gdf['geometry'].apply(lambda x: x.centroid.y)
gdf['longitude'] = gdf['geometry'].apply(lambda x: x.centroid.x)

# Create a density map of the collision events using geopandas' plot method
fig, ax = plt.subplots(figsize=(12, 10))
ax.set_aspect('equal')
base = gdf.plot(ax=ax, alpha=0.5, color='red')
contextily.add_basemap(ax, zoom=18)
ax.set_title('Density Map of Traffic Collisions Resulting in Fatalities or Serious Injuries in Toronto (2006-2021)')
plt.show()

# Set the center of the map to Toronto
map_center = [43.728662, -79.400031]

# Create a folium map centered on Toronto with dark tiles
m = folium.Map(location=map_center, zoom_start=11)

# Add a choropleth layer to the map using the collision events GeoDataFrame
folium.Choropleth(
    geo_data=gdf,
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    name='Collision Events'
).add_to(m)

# Add a LayerControl to the map to toggle the visibility of the collision events layer and the Toronto map layer
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('map.html')

# Define the initial viewport for the map
view_state = pdk.ViewState(latitude=43.6532, longitude=-79.3832, zoom=10)

# Create a layer for the collision events
layer = pdk.Layer(
    'HeatmapLayer',
    data=gdf,
    opacity=0.9,
    get_position='[longitude, latitude]',
    threshold=0.1,
    get_weight=1
)

# Create a Pydeck map with the heatmap layer
view_state = pdk.ViewState(
      latitude=43.728662,
      longitude=-79.400031,
      zoom=9.5,
     pitch=0
)

# Render the map
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html('collision_map.html')

# Create a joint plot showing the density of KSI collisions by longitude and latitude
sns.set_style("white")
sns.jointplot(x='longitude', y='latitude', data=gdf, kind='kde', color='orange')
plt.show()

# Compute the KDE of the collision event coordinates
kde = gaussian_kde(gdf[['longitude', 'latitude']].T)
x, y = np.mgrid[gdf.longitude.min():gdf.longitude.max():100j, gdf.latitude.min():gdf.latitude.max():100j]
z = kde(np.vstack([x.flatten(), y.flatten()]))

# Plot the KDE as a contour plot
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_aspect('equal')
ax.contourf(x, y, z.reshape(x.shape), cmap='Reds')
contextily.add_basemap(ax, zoom=12)
ax.set_title('Kernel Density Estimation of Traffic Collision Events in Toronto (2006-2021)')
plt.show()

# Compute the distance matrix between the collision event coordinates
dist_matrix = squareform(pdist(gdf[['longitude', 'latitude']]))

# Compute the Moran's I statistic using the distance matrix and ObjectId counts
n = len(gdf)
w = dist_matrix / dist_matrix.max()  # Normalize distances to range [0, 1]
w = 1 - w  # Convert distances to spatial weights
w[np.diag_indices(n)] = 0  # Set diagonal weights to 0
moran_i = (n / (2 * (gdf['ObjectId'].sum() / n))) * ((gdf['ObjectId'] - gdf['ObjectId'].mean()) * (w @ (gdf['ObjectId'] - gdf['ObjectId'].mean())) / ((gdf['ObjectId'] - gdf['ObjectId'].mean()) ** 2).sum())

# Plot the Moran's I scatterplot
fig, ax = plt.subplots(figsize=(8, 8))
ax.scatter(gdf.ObjectId, moran_i)
ax.set_xlabel('Number of Collision Events')
ax.set_ylabel("Moran's I")
ax.set_title("Moran's I Scatterplot of Traffic Collision Events in Toronto (2006-2021)")
plt.show()

# Set the base URL for the CKAN instance
base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

# Retrieve the metadata for the traffic-signals-tabular package and its resources
url = base_url + "/api/3/action/package_show"
params = {"id": "traffic-signals-tabular"}
package = requests.get(url, params=params).json()

# Loop through the resources to find the one with datastore_active set to True and retrieve the data in CSV format
for resource in package["result"]["resources"]:
    if resource["datastore_active"]:
        url = base_url + "/datastore/dump/" + resource["id"]
        traffic_signals = pd.read_csv(url)
        break

# Derive the 'LATITUDE' and 'LONGITUDE' columns from the 'geometry' column
traffic_signals['geometry'] = traffic_signals['geometry'].apply(lambda x: json.loads(x))
traffic_signals['LATITUDE'] = traffic_signals['geometry'].apply(lambda x: x['coordinates'][1])
traffic_signals['LONGITUDE'] = traffic_signals['geometry'].apply(lambda x: x['coordinates'][0])

# Derive the latitude and longitude columns from the geometry column of the collision data geodataframe
gdf[['longitude', 'latitude']] = gdf['geometry'].apply(lambda x: pd.Series([x.centroid.x, x.centroid.y]))

# Build a KDTree from the traffic signals for efficient nearest-neighbor lookup
tree = cKDTree(traffic_signals[['LATITUDE', 'LONGITUDE']])

# For each collision, find the distance to the nearest traffic signal
distances, indices = tree.query(gdf[['latitude', 'longitude']].values, k=1)
gdf['DIST_TO_TRAFFIC_SIGNAL'] = distances

# Create a heatmap of the distances to the nearest traffic signal
fig, ax = plt.subplots(figsize=(12, 10))
ax.set_aspect('equal')
gdf.plot(column='DIST_TO_TRAFFIC_SIGNAL', ax=ax, legend=True, cmap='coolwarm_r', alpha=0.7)
contextily.add_basemap(ax, zoom=12)
ax.set_title('Distances to Nearest Traffic Signal for Traffic Collision Events in Toronto (2006-2021)')
plt.show()

# Calculate the average distance to traffic signals for all traffic collisions
average_distance = gdf['DIST_TO_TRAFFIC_SIGNAL'].mean()
print(f'Average distance to nearest traffic signal for traffic collisions: {average_distance:.2f} meters')

# Save the updated GeoDataFrame as a GeoJSON file
gdf.to_file('collision_data_with_nearest_traffic_signal.geojson', driver='GeoJSON')



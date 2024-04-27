import folium

def plot_coordinates(cords):
    """
    Plot a list of latitude and longitude pairs using Folium.

    Args:
    cords (list of tuples): A list where each tuple contains (latitude, longitude).

    Returns:
    folium.Map: A Folium map object with markers added for each coordinate.
    """
    if not cords:
        raise ValueError("The list of coordinates is empty.")
    
    # Calculate the center of the map
    latitudes, longitudes = zip(*cords)
    center_lat = sum(latitudes) / len(latitudes)
    center_lon = sum(longitudes) / len(longitudes)

    # Create a map centered around the calculated center
    map_obj = folium.Map(location=[center_lat, center_lon], zoom_start=6)

    # Add a marker for each coordinate
    for lat, lon in cords:
        folium.Marker([lat, lon], popup=f'({lat}, {lon})').add_to(map_obj)

    return map_obj
"""
# Example usage:
cords = [
    (34.0522, -118.2437),  # Los Angeles
    (36.1699, -115.1398),  # Las Vegas
    (37.7749, -122.4194)   # San Francisco
]

# Generate the map
map_obj = plot_coordinates(cords)

# Save the map to an HTML file
map_obj.save('map.html')
"""


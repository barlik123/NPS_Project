import folium

def create_marker(map_obj, lat, lon, name):
    # Add a marker for each coordinate
    if lat and lon:
        folium.Marker([lat, lon], popup=f'{name}').add_to(map_obj)



import requests
import marker
from Keys import NPS_API_KEY
import geopandas as gpd
from shapely.geometry import Point

states_codes_names = {
    'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming',
}


def get_parks(state_code=None):
    """
    Retrieves all national parks, optionally filtered by a specific state.
    
    Parameters:
    - state_code (str, optional): Two-letter state code to filter parks by a specific state.
    """
    api_base_url = "https://developer.nps.gov/api/v1/parks?"
    all_parks = []
    start = 0
    limit = 50  # Adjust based on what the API supports; 50 is a common limit
    total_parks = None

    while True:
        api_url = f"{api_base_url}start={start}&limit={limit}&api_key={NPS_API_KEY}"
        if state_code:
            api_url += f"&stateCode={state_code}"
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            all_parks.extend(data['data'])
            # Check if total parks count is known, update if not
            if total_parks is None:
                total_parks = int(data['total'])
            # Update start for next page
            start += limit
            if start >= total_parks:
                break
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break

    return all_parks

def is_point_in_state(lat, lon, state_name):
    # Load the US States geometry
    us_states = gpd.read_file('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json')
    # Create a point with your coordinates
    point = Point(lon, lat)
    # Get the geometry of the state from the GeoDataFrame
    state_geom = us_states.loc[us_states['name'] == state_name, 'geometry'].values[0]

    # Check if the point is within the state geometry
    return point.within(state_geom)


def main():
    state_code = input("Enter a state code to filter by (or leave blank for all parks): ").strip().upper()
    if state_code == "":
        state_code = None

    map_obj = folium.Map(location=[39.828156, -98.579362], zoom_start=5)
    parks = get_parks(state_code)
    if state_code:
        parks = get_parks(state_code)
        for park in parks:
            if is_point_in_state(park['latitude'], park['longitude'], states_codes_names[state_code]):
                create_marker(map_obj,park['latitude'],park['longitude'],park['fullName'])
    else:
        parks = get_parks()
        for park in parks:
            create_marker(map_obj,park['latitude'],park['longitude'],park['fullName'])

    map_obj.save(f'{state_code or "ALL_STATES"}.html')

if __name__ == "__main__":
    main()


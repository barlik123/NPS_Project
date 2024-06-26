import requests
from Maps_Testing import *
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
    # file I find on the internet, probably a good idea to find something else later
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

"""
Park in NJ example of dictionaries :
'id':   'FAEF5684-83A4-4CF2-A701-60CF8D4014BD'

'url':   'https://www.nps.gov/appa/index.htm'

'fullName':   'Appalachian National Scenic Trail'

'parkCode':   'appa'

'description':   'The Appalachian Trail is a 2,190+ mile long public footpath that traverses the scenic, wooded, pastoral, wild, and culturally resonant lands of the Appalachian Mountains. Conceived in 1921, built by private citizens, and completed in 1937, today the trail is managed by the National Park Service, US Forest Service, Appalachian Trail Conservancy, numerous state agencies and thousands of volunteers.'

'latitude':   '40.41029575'

'longitude':   '-76.4337548'

'latLong':   'lat:40.41029575, long:-76.4337548'

'activities':   '[{'id': '13A57703-BB1A-41A2-94B8-53B692EB7238', 'name': 'Astronomy'}, {'id': 'D37A0003-8317-4F04-8FB0-4CF0A272E195', 'name': 'Stargazing'}, {'id': 'A59947B7-3376-49B4-AD02-C0423E08C5F7', 'name': 'Camping'}, {'id': '4A58AF13-E8FB-4530-B41A-97DF0B0C77B7', 'name': 'Backcountry Camping'}, {'id': 'C11D3746-5063-4BD0-B245-7178D1AD866C', 'name': 'Compass and GPS'}, {'id': '89DA72D0-16D6-4C1C-89D4-103D94F1F63D', 'name': 'Orienteering'}, {'id': 'B33DC9B6-0B7D-4322-BAD7-A13A34C584A3', 'name': 'Guided Tours'}, {'id': 'A0631906-9672-4583-91DE-113B93DB6B6E', 'name': 'Self-Guided Tours - Walking'}, {'id': '42FD78B9-2B90-4AA9-BC43-F10E9FEA8B5A', 'name': 'Hands-On'}, {'id': '31F88DA6-696F-441F-89CF-D7B1415C4CB9', 'name': 'Citizen Science'}, {'id': '9456A40A-AF75-4AD3-8BE1-79C4A7DBEDFC', 'name': 'Volunteer Vacation'}, {'id': 'BFF8C027-7C8F-480B-A5F8-CD8CE490BFBA', 'name': 'Hiking'}, {'id': '7C37B79B-D02D-49EB-9020-3DB8299B748A', 'name': 'Backcountry Hiking'}, {'id': '45261C0A-00D8-4C27-A1F8-029F933A0D34', 'name': 'Front-Country Hiking'}, {'id': 'DF4A35E0-7983-4A3E-BC47-F37B872B0F25', 'name': 'Junior Ranger Program'}, {'id': '01D717BC-18BB-4FE4-95BA-6B13AD702038', 'name': 'Snowshoeing'}, {'id': '0B685688-3405-4E2A-ABBA-E3069492EC50', 'name': 'Wildlife Watching'}, {'id': '5A2C91D1-50EC-4B24-8BED-A2E11A1892DF', 'name': 'Birdwatching'}]'

'topics':   '[{'id': '0D00073E-18C3-46E5-8727-2F87B112DDC6', 'name': 'Animals'}, {'id': '957EF2BD-AC6C-4B7B-BD9A-87593ADC6691', 'name': 'Birds'}, {'id': 'EC707104-66CB-466F-90F8-76264F3BE578', 'name': 'Horses (wild)'}, {'id': '4DC11D06-00F1-4A01-81D0-89CCCCE4FF50', 'name': 'Climate Change'}, {'id': '41B1A0A3-11FF-4F55-9CB9-034A7E28B087', 'name': 'Forests and Woodlands'}, {'id': '762170E5-0747-4836-B837-7F2547D3F733', 'name': 'Coniferous Forests'}, {'id': 'DE2F0F3C-C0C4-410F-90D3-97EEC33D348E', 'name': 'Deciduous Forests'}, {'id': '1CF1F6BB-A037-445B-8CF2-81428E50CE52', 'name': 'Lakes'}, {'id': '101F4D51-F99D-45A6-BBB6-CD481E5FACED', 'name': 'Mountains'}, {'id': 'F8C2FE93-DEB3-4B12-9A87-913E3E6B448D', 'name': 'Natural Sounds'}, {'id': 'A7359FC4-DAD8-45F5-AF15-7FF62F816ED3', 'name': 'Night Sky'}, {'id': 'E06F3C94-AC8A-4B1C-A247-8EBA8910D5EE', 'name': 'Astronomy'}, {'id': 'A155238F-0DD2-4610-9B87-05FCE1C59283', 'name': 'River and Riparian'}, {'id': '9C9FCBB6-360B-4743-8155-6F9341CBE01B', 'name': 'Scenic Views'}, {'id': '5BE55D7F-BDB6-4E3D-AC35-2D8EBB974417', 'name': 'Trails'}, {'id': 'BA12B386-49EA-46B0-9121-FCACACC47538', 'name': 'Watersheds'}, {'id': '54B56677-1200-4DF1-927C-36F389E04466', 'name': 'Headwaters'}, {'id': '5ED826E0-76BB-47BB-87DD-E081A72B0A04', 'name': 'Waterfalls'}, {'id': '1365C347-952C-475A-B755-731DD523C195', 'name': 'Wetlands'}, {'id': 'B85866E2-0897-4000-9040-605CA335804F', 'name': 'Wilderness'}]'

'states':   'CT,GA,MA,MD,ME,NC,NH,NJ,NY,PA,TN,VA,VT,WV'

'contacts':   '{'phoneNumbers': [{'phoneNumber': '3045356278', 'description': '', 'extension': '', 'type': 'Voice'}], 'emailAddresses': [{'description': '', 'emailAddress': '0@0'}]}'

'entranceFees':   '[]'

'entrancePasses':   '[]'

'fees':   '[]'

'directionsInfo':   'There are many points of access along the Appalachian Trail, whether it is by car, train, bus or plane. For more detailed directions, please refer to the "Directions" section of our park webpage.'

'directionsUrl':   'http://www.nps.gov/appa/planyourvisit/directions.htm'

'operatingHours':   '[{'exceptions': [], 'description': 'In general, the Appalachian Trail is open year-round. The northern terminus at Mount Katahdin in Maine is within Baxter State Park, which may be closed in winter months, depending on weather conditions. \nParticular sections of the Trail, and less-developed roads accessing the Trail, may be closed temporarily for a number of reasons, but otherwise the trail is open.', 'standardHours': {'wednesday': 'All Day', 'monday': 'All Day', 'thursday': 'All Day', 'sunday': 'All Day', 'tuesday': 'All Day', 'friday': 'All Day', 'saturday': 'All Day'}, 'name': 'Appalachian National Scenic Trail'}]'

'addresses':   '[{'postalCode': '25425', 'city': 'Harpers Ferry', 'stateCode': 'WV', 'countryCode': 'US', 'provinceTerritoryCode': '', 'line1': 'Appalachian Trail Park Office', 'type': 'Physical', 'line3': '', 'line2': 'P.O. Box 50'}, {'postalCode': '25425', 'city': 'Harpers Ferry', 'stateCode': 'WV', 'countryCode': 'US', 'provinceTerritoryCode': '', 'line1': 'Appalachian Trail Park Office', 'type': 'Mailing', 'line3': '', 'line2': 'P.O. Box 50'}]'

'images':   '[{'credit': 'Photo Credit: ATC/Benjamin Hays', 'title': 'McAfee Knob', 'altText': 'Silhouette of a man with backpack standing on McAfee Knob at sunset with mountains in the distance.', 'caption': 'McAfee Knob is one of the most popular locations along the A.T. to take photographs.', 'url': 'https://www.nps.gov/common/uploads/structured_data/3C8397D6-1DD8-B71B-0BEF4C54462A1EB3.jpg'}, {'credit': 'Photo Credit: ATC', 'title': 'Appalachian Trail', 'altText': 'The Appalachian Trail runs across a mountain ridge line with views to the horizon of mountain range.', 'caption': 'Crossing into thirteen states, hikers experience a variety of scenery along the way.', 'url': 'https://www.nps.gov/common/uploads/structured_data/3C83A128-1DD8-B71B-0B02DED286AFD8C6.jpg'}, {'credit': 'Photo Credit: ATC/Matthew Davis', 'title': 'The Infamous White Blaze of the A.T.', 'altText': 'A white blaze marks a tree in the foreground, with a man and child walking away on the wooded trail.', 'caption': 'The white blaze marks the Appalachian Trail as a way for hikers to identify the route.', 'url': 'https://www.nps.gov/common/uploads/structured_data/3C83A2B0-1DD8-B71B-0B4589220F4D60D9.jpg'}, {'credit': 'Photo Credit: Maine Appalachian Trail Club', 'title': 'Volunteer on the A.T.', 'altText': 'A volunteer is carrying a split log while walking across a wooden footbridge in the woods.', 'caption': 'The Appalachian Trail is maintained largely by volunteers.', 'url': 'https://www.nps.gov/common/uploads/structured_data/3C83A442-1DD8-B71B-0BD0A5F2BD69B9F6.jpg'}, {'credit': 'Photo Credit: ATC/Greg Walter', 'title': 'Winter on the A.T.', 'altText': 'A snowy winter view from the A.T. overlooking snowy mountains and clouds in the distance.', 'caption': 'Hikers can experience many seasons along the A.T. all year round. It is important to be prepared.', 'url': 'https://www.nps.gov/common/uploads/structured_data/3C83A59A-1DD8-B71B-0BBFB87BBDDAABD6.jpg'}]'

'weatherInfo':   'It is your responsibility to be prepared for all weather conditions, including extreme and unexpected weather changes year-round. As the trail runs from Georgia to Maine there will be different weather conditions depending on your location. For weather along specific sections of the trail and at specific shelters, please refer to: http://www.atweather.org/'

'name':   'Appalachian'

'designation':   'National Scenic Trail'

'multimedia':   '[]'

'relevanceScore':   '1.0'
"""
This Project uses folium, geopandas, and the national parks api to map national parks facilities in a given state (or the entire country).

To use this program you will need to generate your own National Parks api key, to do so check out this website:
https://www.nps.gov/subjects/developer/get-started.htm

You will also need to setup folium and geopandas, you can load them with this command:
pip install geopandas
pip install folium

Now for how it works:
The program is taking a user input of a state's code.
Then it calls the get_parks function which uses the national parks
api to fetch all the the parks that are defined to be in the state.
Afterward we use the is_point_in_state to filter out parks that are 
defined to be in the state but are not actually centered within the state boundaries*.
Finally we plot a marker for each park to be displayed on the map
and create an html file for the map.

*some parks encompass an entire region rather than a state, 
we define those as belonging to the state which they are centered around.

import re
import folium
from folium import IFrame

# Function to parse data from the file
def parse_station_data(file_path):
    data = {
        'latitude': [],
        'longitude': [],
        'number_of_chargers': [],
        'state': [],
        'zip_code': [],
        'connector_types': [],
        'facility': [],
        'owner_type': [],
        'network': [],
        'opening_date': []
    }
    
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Regular expressions for each detail
    lat_long_pattern = r'Location: \(([^,]+), ([^\)]+)\)'
    chargers_pattern = r'Number of Chargers: (\d+)'
    state_pattern = r'State: ([^\n]+)'
    zip_code_pattern = r'Zip Code: (\d+)'
    connector_types_pattern = r'Connector Types: \[([^\]]+)\]'
    facility_pattern = r'Facility: ([^\n]*)'
    owner_type_pattern = r'Owner type: ([^\n]*)'
    network_pattern = r'Network: ([^\n]+)'
    opening_date_pattern = r'Opening date: ([^\n]+)'
    
    # Extracting data
    lat_long_matches = re.findall(lat_long_pattern, content)
    chargers_matches = re.findall(chargers_pattern, content)
    state_matches = re.findall(state_pattern, content)
    zip_code_matches = re.findall(zip_code_pattern, content)
    connector_types_matches = re.findall(connector_types_pattern, content)
    facility_matches = re.findall(facility_pattern, content)
    owner_type_matches = re.findall(owner_type_pattern, content)
    network_matches = re.findall(network_pattern, content)
    opening_date_matches = re.findall(opening_date_pattern, content)
    
    # Process matches
    for match in lat_long_matches:
        try:
            latitude = float(match[0].strip())
            longitude = float(match[1].strip())
            data['latitude'].append(latitude)
            data['longitude'].append(longitude)
        except ValueError as e:
            print(f"Error parsing latitude/longitude: {e}")

    for match in chargers_matches:
        try:
            chargers = int(match.strip())
            data['number_of_chargers'].append(chargers)
        except ValueError as e:
            print(f"Error parsing number of chargers: {e}")
    
    data['state'] = [match.strip() for match in state_matches]
    data['zip_code'] = [match.strip() for match in zip_code_matches]
    data['connector_types'] = [list(set(match.strip().split(', '))) for match in connector_types_matches]
    data['facility'] = [match.strip() for match in facility_matches]
    data['owner_type'] = [match.strip() for match in owner_type_matches]
    data['network'] = [match.strip() for match in network_matches]
    data['opening_date'] = [match.strip() for match in opening_date_matches]

    # Check if data is found
    if not data['latitude'] or not data['longitude']:
        print("No coordinates found in the file.")
    if not data['number_of_chargers']:
        print("Number of chargers not found in the file.")
    if not data['state']:
        print("State information not found in the file.")
    if not data['zip_code']:
        print("Zip Code information not found in the file.")
    if not data['connector_types']:
        print("Connector types information not found in the file.")
    if not data['owner_type']:
        print("Owner type information not found in the file.")
    if not data['opening_date']:
        print("Opening date information not found in the file.")
    
    return data

# Path to the text file with station data
data_file_path = 'C:\\Users\\fakinyemi\\Desktop\\SRELO\\CODE\\combined_city_data.txt'

# Parse the station data from the file
data = parse_station_data(data_file_path)

# Check if we have successfully parsed any coordinates and chargers
if data['latitude'] and data['longitude']:
    # Create a Folium map centered around Chicago
    map_center = [41.8781, -87.6298]
    map_zoom = 10
    map = folium.Map(location=map_center, zoom_start=map_zoom)

    # Define colors based on the number of chargers
    colors = ['red' if chargers < 5 else 'yellow' if chargers < 10 else 'green' for chargers in data['number_of_chargers']]

    # Create markers with popups for each station
    for lat, lon, color, num_chargers, state, zip_code, connector_types, facility, owner_type, network, opening_date in zip(
            data['latitude'], data['longitude'], colors, data['number_of_chargers'], data['state'], data['zip_code'],
            data['connector_types'], data['facility'], data['owner_type'], data['network'], data['opening_date']):
        
        popup_text = (
            f"Number of Chargers: {num_chargers}<br>"
            f"State: {state}<br>"
            f"Zip Code: {zip_code}<br>"
            f"Connector Types: {', '.join(connector_types)}<br>"
            f"Facility: {facility}<br>"
            f"Owner Type: {owner_type}<br>"
            f"Network: {network}<br>"
            f"Opening Date: {opening_date}"
        )
        
        # Create a marker with a popup
        folium.CircleMarker(
            location=[lat, lon],
            color=color,
            radius=7,
            fill=True,
            fill_color=color,
            fill_opacity=0.3,
            popup=folium.Popup(popup_text, max_width=300)
        ).add_to(map)
    
    # Path to save the generated HTML file
    html_file_path = 'C:\\Users\\fakinyemi\\Desktop\\click_EV_map.html'
    
    # Create the directory if it doesn't exist
    import os
    os.makedirs(os.path.dirname(html_file_path), exist_ok=True)
    
    # Save the map
    map.save(html_file_path)
    
    print(f"Map has been created and saved to {html_file_path}")
else:
    print("Insufficient data to create the map.")

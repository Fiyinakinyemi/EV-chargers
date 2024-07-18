import os
import requests

# Define the API key and endpoint
api_key = 'Tp58hOiBmX5I0BeSz1liCyXZnlCvRHmmzUd6gNhh' 
nrel_endpoint = 'https://developer.nrel.gov/api/alt-fuel-stations/v1.json'

# Function to safely convert a value to integer or return 0 if conversion fails
def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

# Function to get the owner type description from the abbreviation letters
def get_owner_type_description(owner_type):
    owner_type_mapping = {
        'FG': 'Federal Government Owned',
        'J': 'Jointly Owned',
        'LG': 'Local/Municipal Government Owned',
        'P': 'Privately Owned',
        'SG': 'State/Provincial Government Owned',
        'T': 'Utility Owned',
        'all': 'All'
    }
    
    # Split the input by commas to handle multiple owner types
    owner_types = owner_type.split(',')
    
    # Get the full description for each owner type and join them with commas
    descriptions = [owner_type_mapping.get(ot.strip(), 'Unknown') for ot in owner_types]
    
    return ', '.join(descriptions)

# Set up the parameters for the NREL API request
nrel_params = {
    'api_key': api_key,
    'fuel_type': 'ELEC',
    'status': 'E',  # Only open stations
    'country': 'US',
    # Assuming we are setting a bounding box for Chicago area
    #'latitude_min': 41.6445,  # Southern boundary of Chicago
    #'longitude_min': -87.9401,  # Western boundary of Chicago
    #'latitude_max': 42.0230,  # Northern boundary of Chicago
    #'longitude_max': -87.5240,  # Eastern boundary of Chicago (Lake Michigan)
    #'limit': 200  # Adjust as necessary
}

# Make the NREL API request
nrel_response = requests.get(nrel_endpoint, params=nrel_params)

# Check if the NREL request was successful
if nrel_response.status_code == 200:
    nrel_data = nrel_response.json()
    
    # Prepare data lines for writing to file
    data_lines = []
    
    # Get the total number of stations for all fuel types
    if 'total' in nrel_data:
        total_stations = nrel_data['total']
        data_lines.append(f"Total Stations (all fuel types): {total_stations}")
    
    # Print the details of each electric charging station
    stations = nrel_data.get('fuel_stations', [])
    if stations:
        electric_stations = [station for station in stations if station.get('fuel_type_code', '') == 'ELEC' and station.get('state', '') == 'IL'and (station.get('zip', '').startswith('606') or station.get('zip', '').startswith('607') or station.get('zip', '').startswith('608'))]
        data_lines.append(f"Total Electric Charging Stations in Chicago: {len(electric_stations)}")
        
        for station in electric_stations:
            station_name = station.get('station_name', 'Unknown')
            latitude = station.get('latitude', 'Unknown')
            longitude = station.get('longitude', 'Unknown')
            zip_code = station.get('zip', 'Unknown')
            ev_connector_types = station.get('ev_connector_types', 'Unknown')
            ev_network = station.get('ev_network', 'Unknown')  # Assuming this is the installer field
            ev_facility = station.get('facility_type', 'Unknown')
            ev_owner = station.get('owner_type', 'Unknown')
            ev_state = station.get('state', 'Unknown')
            owner_description = get_owner_type_description(ev_owner)
            ev_date = station.get('open_date', 'Unknown')
            ev_level1_evse_num = safe_int(station.get('ev_level1_evse_num', 0))  # Number of chargers
            ev_level2_evse_num = safe_int(station.get('ev_level2_evse_num', 0))  # Number of chargers
            ev_dc_fast_num = safe_int(station.get('ev_dc_fast_num', 0))  # Number of chargers
            ev_other_evse = safe_int(station.get('ev_other_evse', 0))  # Number of chargers
            
            # Calculate total number of chargers
            total_chargers = ev_level1_evse_num + ev_level2_evse_num + ev_dc_fast_num + ev_other_evse
            
            data_lines.append(f"Station Name: {station_name}")
            data_lines.append(f"  Location: ({latitude}, {longitude})")
            data_lines.append(f"  State: {ev_state}")
            data_lines.append(f"  Zip Code: {zip_code}")
            data_lines.append(f"  Connector Types: {ev_connector_types}")
            data_lines.append(f"  Facility: {ev_facility}")
            data_lines.append(f"  Owner type: {owner_description}")
            data_lines.append(f"  Network: {ev_network}")
            data_lines.append(f"  Opening date: {ev_date}")
            data_lines.append(f"  Number of Chargers: {total_chargers}\n")
    
    else:
        data_lines.append("No charging stations found within the specified route and distance.")

    # Write data to a file in the current directory
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, 'chicago_ev_stations.txt')

        with open(file_path, 'w', encoding='utf-8') as file:
            for line in data_lines:
                file.write(line + '\n')

        print(f"Data has been written to {file_path}")

    except IOError as e:
        print(f"Error writing to the file: {e}")

else:
    print(f"Failed to retrieve data: {nrel_response.status_code}")

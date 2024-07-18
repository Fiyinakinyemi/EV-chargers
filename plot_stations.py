import os
import re
import gmplot

# Function to parse latitude, longitude, and number of chargers from the file
def parse_lat_long_chargers(file_path):
    latitude_list = []
    longitude_list = []
    chargers_list = []
    
    with open(file_path, 'r') as file:
        station_data = file.read()
        
    # Regular expressions to find latitude, longitude, and number of chargers
    lat_long_pattern = r'Location: \(([^,]+), ([^\)]+)\)'
    chargers_pattern = r'Number of Chargers: (\d+)'
    
    # Find all matches for latitude and longitude
    lat_long_matches = re.findall(lat_long_pattern, station_data)
    print(f"the total {len(lat_long_matches)}")
    chargers_matches = re.findall(chargers_pattern, station_data)
    # Process latitude and longitude matches
    for match in lat_long_matches:
        try:
            latitude = float(match[0].strip())
            longitude = float(match[1].strip())
            latitude_list.append(latitude)
            longitude_list.append(longitude)
        except ValueError as e:
            print(f"Error parsing latitude/longitude: {e}")
    
    # Process number of chargers matches
    for match in chargers_matches:
        try:
            chargers = int(match.strip())
            chargers_list.append(chargers)
        except ValueError as e:
            print(f"Error parsing number of chargers: {e}")
    
    return latitude_list, longitude_list, chargers_list

# Path to the text file with station data
data_file_path = 'C:\\Users\\fakinyemi\\Desktop\\SRELO\\CODE\\combined_city_data.txt'

# Parse the latitude, longitude, and number of chargers from the file
latitude_list, longitude_list, chargers_list = parse_lat_long_chargers(data_file_path)

# Check if we have successfully parsed any coordinates and chargers
if not latitude_list or not longitude_list:
    print("No coordinates found in the file.")
if not chargers_list:
    print("Number of chargers not found in file")
else:

    # Create the GoogleMapPlotter object centered around Chicago
    gmap3 = gmplot.GoogleMapPlotter(41.8781, -87.6298, 10)  # Centered around Chicago

    # Define colors based on the number of chargers
    colors = ['#FF0000' if chargers < 5 else '#FFFF00' if chargers < 10 else '#00FF00' for chargers in chargers_list]

    # Scatter the points on the map with the corresponding colors
    for lat, lon, color in zip(latitude_list, longitude_list, colors):
        gmap3.scatter([lat], [lon], color, size=40, marker=False)

    # Path to save the generated HTML file
    html_file_path = 'C:\\Users\\fakinyemi\\Desktop\\Chicago_EV_map.html'

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(html_file_path), exist_ok=True)

    # Draw the map
    gmap3.draw(html_file_path)

    print(f"Map has been created and saved to {html_file_path}")
    

import pandas as pd
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import time
import re

#this scrapper using edge broser
#download the driver: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH#downloads

# Define Edge WebDriver path
service = Service(r'E:/projects/python/GoogleScrapper/edgedriver_win64/msedgedriver.exe')  # Adjust to your Edge WebDriver path
options = webdriver.EdgeOptions()
options.add_argument('--headless')  # Run in headless mode if desired

# Initialize Edge WebDriver with specified service and options
driver = webdriver.Edge(service=service, options=options)

# Function to extract latitude and longitude
def extract_lat_long(url):
    driver.get(url)
    time.sleep(3)  # Give some time for the page to load fully

    # Get the updated URL after the page loads
    current_url = driver.current_url

    # Extract latitude and longitude from the URL using regex
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', current_url)
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude, longitude
    else:
        return None, None

# Load URLs from the existing CSV
input_file = 'combined_places.csv'  # Path to your input CSV file
output_file = 'combined_places_With_locations.csv'  # Path for saving the updated CSV

# Read the CSV file into a DataFrame
df = pd.read_csv(input_file)
print(df.columns)
# Add new columns for latitude and longitude, defaulting to None
df['latitude'] = None
df['longitude'] = None


#here we should split the task to make it faster for us:

# Loop through each URL in the DataFrame and extract coordinates
for index, row in df.iterrows():
    url = row['url']
    print(url)

    lat, long = extract_lat_long(url)
    df.at[index, 'latitude'] = lat
    df.at[index, 'longitude'] = long
    print(f"Processed URL: {url}, Latitude: {lat}, Longitude: {long}")

# Close the browser
driver.quit()

# Save the updated DataFrame to a new CSV file (or overwrite the original file if desired)
df.to_csv(output_file, index=False)
print(f"Results saved to {output_file}")

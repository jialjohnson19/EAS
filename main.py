
# import libraries 
from src.setup import geocode_address
from src.map_setup import create_leaflet_subject_map

import webbrowser
import os




######### beginning of code ########
# address = input("Enter the address of the subject property: ")

#standing address for testing 
# standing address for testing
address = "2632 Central Avenue, St. Petersburg, FL"

# PRINT ADDRESS TO BE GEOCODED
result = geocode_address(address)

# PATH TO MAP 
map_path = create_leaflet_subject_map(result)


# OPEN BROWSER TO VIEW MAP
webbrowser.open(
    "file://" + os.path.abspath(map_path)
)
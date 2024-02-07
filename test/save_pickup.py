from geopy.geocoders import Nominatim
import chronopost as chro
import mondial as mond
import json
def get_geocode(address):
    geolocator = Nominatim(user_agent='user')
    location = geolocator.geocode(address)
    return float(location.raw['lat']), float(location.raw['lon'])

number = "4"
street = "rue Fonderie Vieille"
zipcode = "13002"
city = "Marseille"
country = "France"

address = ', '.join([number, street, zipcode, city, country])

lat, lon = get_geocode(address)
colissimo_pup = chro.get_colissimo_pickup_points(lat, lon, zipcode, city, country)[0]
mondial_pup = mond.get_mondial_pickup_points(zipcode, city)[0]

with open("pu_points.json", "w") as outfile:
    json.dump([{'latitude':lat, 'longitude':lon}, colissimo_pup, mondial_pup], outfile, indent=4)
    # json.dump(mondial_pup, outfile, indent=4)
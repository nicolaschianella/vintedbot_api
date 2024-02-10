from geopy.geocoders import Nominatim
import chronopost as chro
import mondial as mond
import json

def get_geocode(address):
    geolocator = Nominatim(user_agent='user')
    location = geolocator.geocode(address)
    return float(location.raw['lat']), float(location.raw['lon'])

number = "4"
street = "rue fonderie vieille"
zipcode = "13002"
city = "marseille"
country = "france"

address = ', '.join([number, street, zipcode, city, country])

lat, lon = get_geocode(address)

colissimo_pup = chro.get_colissimo_pickup_points(lat, lon, zipcode, city, country)[0]
mondial_pup = mond.get_mondial_pickup_points(zipcode, city)[0]

with open("pu_points.json", "w") as outfile:
    json.dump([{'latitude':lat, 'longitude':lon},
               {'chronopost_pup_latitude':float(colissimo_pup['latitude']), 'chronopost_pup_longitude':float(colissimo_pup['longitude'])},
               {'mondial_pup_latitude':mondial_pup['Adresse']['Latitude'], 'mondial_pup_longitude':mondial_pup['Adresse']['Longitude']}],
              outfile, indent=4)
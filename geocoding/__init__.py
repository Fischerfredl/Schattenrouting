from geopy.exc import GeopyError
from geopy.geocoders import Nominatim, GoogleV3


def geolocate_query(query):
    geolocator = Nominatim(format_string='%s, Augsburg, Deutschland')
    location = geolocator.geocode(query)
    coords = None
    if location:
        address, coords = location
    return coords


def geolocate_coords(coord):
    geolocator = Nominatim()
    address = 'No address found'
    location = geolocator.reverse(str(coord[0])+', '+str(coord[1]), exactly_one=True)
    if location:
        found = location.address.split(',')
        address = found[1].strip(' ') + ' ' + found[0]

    return address


def get_timezone(coords):
    g = GoogleV3()
    timezone = g.timezone(coords)
    return timezone

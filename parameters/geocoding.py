from geopy.exc import GeopyError
from geopy.geocoders import Nominatim, GoogleV3
from format_data import get_in_bounds


def geolocate_query(query):
    geolocator = Nominatim(format_string='%s, Augsburg, Deutschland')
    location = geolocator.geocode(query)
    if location:
        address, coords = location
    else:
        raise GeopyError('No result found')
    return get_in_bounds(coords)


def geolocate_coords(coord):
    geolocator = Nominatim()
    address = 'No address found'
    location = geolocator.reverse(str(coord[0])+', '+str(coord[1]), exactly_one=True)
    if location:
        address = location.address.split(',')
    return address[1]+' '+address[0]


def get_timezone(coords):
    g = GoogleV3()
    timezone = g.timezone(coords)
    return timezone

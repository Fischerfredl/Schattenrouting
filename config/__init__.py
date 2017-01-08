import os
import random
random = random.SystemRandom()


def set_config(app):
    for key in config.keys():
        app.config[key] = config[key]
    return


def get_secret_key(length=50, allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                            'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                                            '0123456789!@#$%^&*(-_=+)'):
    return ''.join(random.choice(allowed_chars) for i in range(length))

config = {
    'GOOGLEMAPS_KEY': 'AIzaSyDdSwma5Rv0hPcgHwPCzy59WbHIgJSZIMg',
    'DEFAULT_START': (48.366544, 10.894866),
    'DEFAULT_END': (48.366544, 10.902866),
    'DEFAULT_BOUNDS': {'north': 48.3826663, 'south': 48.351494, 'west': 10.8733938, 'east': 10.9188537},
    'SECRET_KEY': get_secret_key(),
    'DATABASE': os.path.abspath('Database/database.db'),
    'OSM_INPUT': os.path.abspath('Datasource/map.osm'),
    'OSM_OUTPUT': os.path.abspath('Datasource/output.osm'),
    'KML_Input': os.path.abspath('Datasource/Augsburg.kml'),
    'IPADDR': '10.4.9.62',
    'PORT': 5000
}

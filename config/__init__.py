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
    'SECRET_KEY': get_secret_key(),
    'DATABASE': os.path.abspath('Database/database.db'),
    'OSM_INPUT': os.path.abspath('Datasource/map.osm'),
    'OSM_OUTPUT': os.path.abspath('Datasource/output.osm'),
    'KML_Input': os.path.abspath('Datasource/Augsburg.kml'),
    'IPADDR': '0.0.0.0',
    'PORT': 5000
}

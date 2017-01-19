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
    'IPADDR': '0.0.0.0',
    'PORT': 5000
}

bounds = {
    'west': 10.877044240271672,
    'east': 10.915640681173187,
    'north': 48.381499267422946,
    'south': 48.35354955784755
}

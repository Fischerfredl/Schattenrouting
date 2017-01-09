from flask import session
from datetime import datetime


def get_in_bounds(coords):
    lat = coords[0]
    lon = coords[1]
    bounds = session['bounds']
    lat = bounds['south'] if lat < bounds['south'] else lat
    lat = bounds['north'] if lat > bounds['north'] else lat
    lon = bounds['west'] if lon < bounds['west'] else lon
    lon = bounds['east'] if lon > bounds['east'] else lon
    coords = (lat, lon)
    return coords


def check_parameter(coord_str):
    lat, lon = coord_str.split(',')
    coords = (float(lat), float(lon))
    coords = get_in_bounds(coords)
    return coords


def format_time(date, time):
    return datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M')

from datetime import datetime
from flask import session, flash, request
from config import config
from queries import get_bounds


def set_coords(what, coord_str):
    try:
        lat, lon = coord_str.split(',')
        f_lat = float(lat)
        f_lon = float(lon)
        bounds = config['bounds']
        out_of_scope = 0
        if f_lat < bounds['south']:
            out_of_scope = 1
            f_lat = bounds['south']
        if f_lat > bounds['north']:
            out_of_scope = 1
            f_lat = bounds['south']
        if f_lon < bounds['west']:
            out_of_scope = 1
            f_lon = bounds['west']
        if f_lon > bounds['east']:
            out_of_scope = 1
            f_lon = bounds['east']
        session[what] = (f_lat, f_lon)
        if out_of_scope == 1:
            flash(what+'-Coordinates were out of scope')
    except ValueError as e:
        print what+'-Koordinaten konnten nicht gelesen werden'
        print e.message
    return


def set_date(date_str):
    try:
        session['date'] = datetime.strptime(date_str, '%Y.%m.%d-%H:%M')
    except ValueError as e:
        print 'Datum konnte nicht gesetzt werden'
        print e.message
    return


def init():
    params = {
        'start': config['DEFAULT_START'],
        'end': config['DEFAULT_END'],
        'date': datetime.utcnow(),
        'rect': False,
        'bldg': False,
        'routes': False,
        'nds': False,
        'shortest': False
    }
    for key in params:
        if not session.get(key):
            session[key] = params[key]

    config['date'] = datetime.utcnow()

    if not config.get('bounds'):
        config['bounds'] = get_bounds()

    start = request.args.get('start', None)
    end = request.args.get('end', None)
    date = request.args.get('date', None)

    if start:
        set_coords('start', start)
    if end:
        set_coords('end', end)
    if date:
        set_date(date)
    return


def process_post():
    if 'toggle_rect' in request.form:
        session['rect'] = not session['rect']
    if 'toggle_bldg' in request.form:
        session['bldg'] = not session['bldg']
    if 'toggle_routes' in request.form:
        session['routes'] = not session['routes']
    if 'toggle_nds' in request.form:
        session['nds'] = not session['nds']
    if 'toggle_shortest' in request.form:
        session['shortest'] = not session['shortest']
    if request.form.get('set_coords'):
        set_coords('start', request.form['set_coords_start'])
        set_coords('end', request.form['set_coords_end'])

from datetime import datetime
from flask import session, request
from queries import get_bounds
from geocoding import geolocate_coords, geolocate_query, get_timezone
from geopy.exc import GeopyError
from format_data import check_parameter, format_time


def init():
    params = {
        'start': (48.3645044, 10.8891771),
        'end': (48.3709503, 10.9091661),
        'start_addr': '',
        'end_addr': '',
        'date': None,
        'rect': True,
        'bldg': False,
        'routes': False,
        'nds': False,
        'shortest': True,
        'shadiest': False,
        'bounds': get_bounds()
    }
    for key in params:
        if not key in session:
            session[key] = params[key]

    session['date'] = datetime.now(get_timezone(session['start'])).replace(tzinfo=None)

    process_args()

    try:
        session['start_addr'] = geolocate_coords(session['start'])
        session['end_addr'] = geolocate_coords(session['end'])
    except GeopyError as e:
        print 'Something went wrong on geocoding coordinates'
        print e.message
    return


def process_args():
    start = request.args.get('start', None)
    end = request.args.get('end', None)

    if start:
        try:
            session['start'] = check_parameter(start)
        except ValueError as e:
            print 'URL parameter start-coordinates could not be read'
            print e.message
    if end:
        try:
            session['end'] = check_parameter(end)
        except ValueError as e:
            print 'URL parameter end-coordinates could not be read'
            print e.message
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
    if 'toggle_shadiest' in request.form:
        session['shadiest'] = not session['shadiest']
    if request.form.get('set_coords'):
        start = request.form['set_coords_start']
        end = request.form['set_coords_end']
        try:
            session['start'] = check_parameter(start)
        except ValueError:
            try:
                session['start'] = geolocate_query(start)
            except GeopyError as e:
                print 'Input start-coordinates could not be read'
                print e
        try:
            session['end'] = check_parameter(end)
        except ValueError:
            try:
                session['end'] = geolocate_query(end)
            except GeopyError as e:
                print 'Input end-coordinates could not be read'
                print e.message
    if request.form.get('set_date'):
        try:
            session['date'] = format_time(request.form['input_date'], request.form['input_time'])
        except ValueError as e:
            print 'Input date could not be read'
            print e.message
    return

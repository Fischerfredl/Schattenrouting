from flask_googlemaps import Map
from flask import session
from map_objects import rectangle, bldg, routes, nds, shortest, shadiest


def build_map():
    markers = [(session.get('start')[0], session.get('start')[1], '<b>Start:</b><br>'+session['start_addr']),
               (session.get('end')[0], session.get('end')[1], '<b>Ziel:</b><br>'+session['end_addr'])]
    rectangles = None
    if session.get('rect'):
        rectangles = [rectangle()]
    polygons = None
    if session.get('bldg'):
        polygons = bldg()
    polylines = []
    if session.get('routes'):
        polylines.extend(routes())
    if session.get('nds'):
        markers.extend(nds())
    if session.get('shortest'):
        polylines.append(shortest())
    if session.get('shadiest'):
        polylines.append(shadiest())
    return Map(
        identifier="map",
        lat=session.get('start')[0],
        lng=session.get('start')[1],
        zoom=14,
        markers=markers,
        rectangles=rectangles,
        polylines=polylines,
        polygons=polygons,
        style='',
        zoom_control=True,
        maptype_control=True,
        scale_control=True,
        streetview_control=False,
        rotate_control=False,
        scroll_wheel=True,
        fullscreen_control=False,
    )

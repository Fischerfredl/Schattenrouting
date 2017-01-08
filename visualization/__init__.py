from flask import session, url_for
from flask_googlemaps import Map
from data.kml_coordinates import coords_to_array
from queries import get_nodes, get_graph, get_buildings
from external.dijkstra import shortestPath
from find_node import find_node
from node_infobox import html
from config import config


def rectangle():
    bounds = config['bounds']
    return {
        'stroke_color': '#00603F',
        'stroke_opacity': 1.,
        'stroke_weight': 4,
        'fill_color': '#FFFFFF',
        'fill_opacity': .1,
        'bounds': {
            'north': bounds['north'],
            'south': bounds['south'],
            'east': bounds['east'],
            'west': bounds['west']
        }
    }


def routes():
    # Note: Duplicate-checking too cost expensive
    graph, nodes = get_graph()
    polylines = []
    for start_id in graph:
        for end_id in graph[start_id]:
            start = nodes[start_id]
            end = nodes[end_id]
            polyline = {
                'stroke_color': '#EF301F',
                'stroke_opacity': 0.9,
                'stroke_weight': 1,
                'path': [start, end]
            }
            polylines.append(polyline)
    return polylines


def shadiest():
    graph, nodes = get_graph()
    polyline = {
        'stroke_color': '#000000',
        'stroke_opacity': 0.9,
        'stroke_weight': 5,
        'path': []
    }

    start = find_node(session['start'])
    end = find_node(session['end'])
    if start and end:
        for node_id in shortestPath(graph, start, end):
            polyline['path'].append(nodes[node_id])
    return polyline


def shortest():
    graph, nodes = get_graph()
    polyline = {
        'stroke_color': '#000000',
        'stroke_opacity': 0.9,
        'stroke_weight': 5,
        'path': []
    }

    start = find_node(session['start'])
    end = find_node(session['end'])
    if start and end:
        for node_id in shortestPath(graph, start, end):
            polyline['path'].append(nodes[node_id])
    return polyline


def bldg():
    polygons = []
    for building in get_buildings():
        coords = coords_to_array(building[5])
        polygon = {
            'stroke_color': '#00603F',
            'stroke_opacity': 0.7,
            'stroke_weight': 1,
            'fill_color': '#53c49d',
            'fill_opacity': .5,
            'path': coords
        }
        polygons.append(polygon)
    return polygons


def nds():
    markers = []
    nodes = get_nodes()
    for node in nodes:
        lat = nodes[node][0]
        lon = nodes[node][1]
        marker = {
            'icon': url_for('static', filename='icons/node8.png'),
            'lat': lat,
            'lng': lon,
            'infobox': html(lat, lon)
        }
        markers.append(marker)
    return markers


def build_map():
    markers = [(session.get('start')[0], session.get('start')[1], 'Start')]
    if session.get('end'):
        markers.append((session.get('end')[0], session.get('end')[1], 'Ziel'))
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

from flask import session, url_for
from data.kml_coordinates import coords_to_array
from queries import get_nodes, get_graph, get_buildings
from external.dijkstra import shortestPath
from find_node import find_node


def rectangle():
    bounds = session['bounds']
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
        'stroke_color': '#005071',
        'stroke_opacity': 0.9,
        'stroke_weight': 5,
        'path': []
    }
    for node_id in shortestPath(graph, find_node(session['start']), find_node(session['end'])):
        polyline['path'].append(nodes[node_id])
    return polyline


def shortest():
    graph, nodes = get_graph()
    polyline = {
        'stroke_color': '#00B3FD',
        'stroke_opacity': 0.9,
        'stroke_weight': 5,
        'path': []
    }
    for node_id in shortestPath(graph, find_node(session['start']), find_node(session['end'])):
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
            'infobox': '('+str(lat)+','+str(lon)+')'
                       '<a href="'+url_for('index', start=str(lat)+','+str(lon))+'">Route from here</a><br>'
                       '<a href="'+url_for('index', end=str(lat)+','+str(lon))+'">Route to here</a>'
        }
        markers.append(marker)
    return markers

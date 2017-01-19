from flask import session, url_for
from external.dijkstra import shortestPath
from find_node import find_node
from queries import get_nodes, get_graph, get_buildings, get_shadow, get_bounds


def coords_to_array(coords):
    coord_array = []
    for c in coords.strip().split(';'):
        x, y = c.split(',')
        coord_array.append((float(x), float(y)))
    return coord_array


def rectangle():
    bounds = get_bounds()
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
            polylines.append({
                'stroke_color': '#EF301F',
                'stroke_opacity': 0.9,
                'stroke_weight': 1,
                'path': [nodes[start_id], nodes[end_id]]
            })
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
        polygons.append({
            'stroke_color': '#00603F',
            'stroke_opacity': 0.7,
            'stroke_weight': 1,
            'fill_color': '#53c49d',
            'fill_opacity': .5,
            'path': coords_to_array(building[5])
        })
    return polygons


def nds():
    markers = []
    nodes = get_nodes()
    for node in nodes:
        lat = nodes[node][0]
        lon = nodes[node][1]
        markers.append({
            'icon': url_for('static', filename='icons/node8.png'),
            'lat': lat,
            'lng': lon,
            'infobox': '('+str(lat)+','+str(lon)+')'
                       '<a href="'+url_for('index', start=str(lat)+','+str(lon))+'">Route from here</a><br>'
                       '<a href="'+url_for('index', end=str(lat)+','+str(lon))+'">Route to here</a>'
        })
    return markers


def shadow_map():
    polygons = []
    for polygon in get_shadow():
        polygons.append({'stroke_color': '#000000',
                         'stroke_opacity': 0.3,
                         'stroke_weight': 1,
                         'fill_color': '#000000',
                         'fill_opacity': .3,
                         'path': polygon
                         })
    return polygons

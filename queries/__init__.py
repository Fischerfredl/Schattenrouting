import sqlite3
import numpy as np
from external.dijkstra import shortestPath


# Query database -------------------------------------------------------------------------------------------------------

def query_db(query, args=()):
    connection = sqlite3.connect('Database/database.db')
    cur = connection.cursor().execute(query, args)
    return cur.fetchall()


# Utils ----------------------------------------------------------------------------------------------------------------

def lin_ab(x, a, b, A, B):
    return A+(x-a)*(B-A)/(b-a)


def get_dist(coords_start, coords_end):
    lat1 = coords_start[0]
    lon1 = coords_start[1]
    lat2 = coords_end[0]
    lon2 = coords_end[1]
    lat = ((lat1 + lat2)/2)
    dx = 111.3 * np.cos(lat*(np.pi/180)) * (lon1-lon2)
    dy = 111.3 * (lat1-lat2)
    return np.sqrt(dx*dx+dy*dy)


def find_node(coords):
    node = None
    dist = float('inf')
    nodes = get_nodes()
    for iter_node in nodes:
        iter_dist = get_dist(coords, nodes[iter_node])
        if iter_dist < dist:
            node = iter_node
            dist = iter_dist
    return node


def parse_polygon(poly_str):
    polygon = []
    for coordinate in poly_str.split(';'):
        lat, lng = coordinate.split(',')
        polygon.append({'lat': float(lat), 'lng': float(lng)})
    return polygon


def get_grid_id(date):
    day = int(date.strftime('%j'))
    hour = date.hour
    minute = date.minute
    grid_id = query_db('SELECT GridID FROM Date WHERE DAY = ? AND Hour = ? AND Minute = ?', [day, hour, minute])
    return grid_id[0][0] if grid_id else None


def get_weighted(grid_id):
    weighted = dict()
    if grid_id:
        for row in query_db('SELECT GraphID, Factor FROM Weighted WHERE GridID = ?', [grid_id]):
            weighted[row[0]] = row[1]
        return weighted
    else:
        return None

# Get-Methods ----------------------------------------------------------------------------------------------------------


def get_nodes():
    all_nodes = {}
    for node in query_db('SELECT * FROM Nodes'):
        all_nodes[node[0]] = (node[1], node[2])
    return all_nodes


def get_solar_position(date):
    query = query_db('SELECT Azimut, Elevation FROM Grid WHERE GridID = ?', [get_grid_id(date)])
    return (query[0][0], query[0][1]) if query else (0, 0)


# Getter for JavaScript ------------------------------------------------------------------------------------------------

def get_bounds():
    bounds = dict()
    bounds['north'] = query_db('SELECT Value FROM Bounds WHERE Direction = "North"')[0][0]
    bounds['south'] = query_db('SELECT Value FROM Bounds WHERE Direction = "South"')[0][0]
    bounds['west'] = query_db('SELECT Value FROM Bounds WHERE Direction = "West"')[0][0]
    bounds['east'] = query_db('SELECT Value FROM Bounds WHERE Direction = "East"')[0][0]
    return bounds


# data

def get_buildings():
    return [parse_polygon(row[0]) for row in query_db('SELECT Polygon FROM Buildings')]


def get_shadow(date):
    grid_id = get_grid_id(date)

    if grid_id:
        return [parse_polygon(row[0])for row in query_db('SELECT Polygon FROM Shadow WHERE GridID = ?', [grid_id])]
    else:
        bounds = get_bounds()
        return [[{'lat': bounds['north'], 'lng': bounds['west']}, {'lat': bounds['north'], 'lng': bounds['east']},
                {'lat': bounds['south'], 'lng': bounds['east']}, {'lat': bounds['south'], 'lng': bounds['west']},
                {'lat': bounds['north'], 'lng': bounds['west']}]]


def get_graph_visualization(date):
    weighted = get_weighted(get_grid_id(date))

    lines = []
    nodes = get_nodes()

    dub_checker = set()
    for edge in query_db('SELECT GraphID, FromID, ToID, Costs FROM Graph'):
        start = nodes[edge[1]]
        end = nodes[edge[2]]
        factor = 1 if not weighted else weighted[edge[0]]
        factor_str = '#' + str(format(int(lin_ab(factor, 1., 10., 0., 255.)), 'x') * 3)
        if str(end) + str(start) not in dub_checker:
            lines.append(({'lat': start[0], 'lng': start[1]}, {'lat': end[0], 'lng': end[1]}, factor_str))
        dub_checker.add(str(start) + str(end))
    return lines


# paths

def get_graph(date, start, end, case):
    weighted = get_weighted(get_grid_id(date))

    path = []
    nodes = get_nodes()
    graph = dict()
    for edge in query_db('SELECT FromID, ToID, GraphID, Costs FROM Graph'):
        node1 = edge[0]
        node2 = edge[1]
        factor = 1
        if case == 'shadiest':
            factor = 1 if not weighted else lin_ab(weighted[edge[2]], 1., 10., 1., 3.)
        elif case == 'sunniest':
            factor = 1 if not weighted else lin_ab(10 - weighted[edge[2]], 1., 10., 1., 2.)
        cost = edge[3] * factor
        if not graph.get(node1):
            graph[node1] = {node2: cost}
        else:
            graph[node1][node2] = cost

    for node_id in shortestPath(graph, find_node(start), find_node(end)):
        node = nodes[node_id]
        path.append({'lat': node[0], 'lng': node[1]})
    return path




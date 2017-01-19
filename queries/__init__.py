import sqlite3
from config import config
from flask import session


def query_db(query, args=()):
    connection = sqlite3.connect(config['DATABASE'])
    cur = connection.cursor().execute(query, args)
    return cur.fetchall()


def get_bounds():
    bounds = dict()
    bounds['north'] = query_db('SELECT Value FROM Bounds WHERE Direction == "North"')[0][0]
    bounds['south'] = query_db('SELECT Value FROM Bounds WHERE Direction = "South"')[0][0]
    bounds['west'] = query_db('SELECT Value FROM Bounds WHERE Direction = "West"')[0][0]
    bounds['east'] = query_db('SELECT Value FROM Bounds WHERE Direction = "East"')[0][0]
    return bounds


def get_nodes():
    all_nodes = {}
    try:
        for node in query_db('SELECT * FROM Nodes'):
            all_nodes[node[0]] = (node[1], node[2])
    except sqlite3.Error as e:
        print 'SQL-Error: Not able to load <Nodes> from Database'
        print e.message
    return all_nodes


def get_buildings():
    polygons = []
    for row in query_db('SELECT Polygon FROM Buildings'):
        polygons.append([(float(coordinate.split(',')[0]), float(coordinate.split(',')[1]))
                         for coordinate in row[0].split(';')])
    return polygons


def get_shadow(date=session['date']):
    day = int(date.strftime('%j'))
    hour = date.hour
    minute = date.minute

    grid_id = query_db('SELECT GridID FROM Date WHERE DAY = ? AND Hour = ? AND Minute = ?', [day, hour, minute])

    polygons = []

    if grid_id:
        for row in query_db('SELECT Polygon FROM Shadow WHERE GridID = ?', [grid_id]):
            polygons.append([(float(coordinate.split(',')[0]), float(coordinate.split(',')[1]))
                             for coordinate in row[0].split(';')])
    else:
        bounds = get_bounds()
        p = [(bounds['north'], bounds['west']), (bounds['north'], bounds['east']),
             (bounds['south'], bounds['east']), (bounds['south'], bounds['west']), (bounds['north'], bounds['west'])]
        polygons.append(p)
    return polygons


def get_graph(date=session['date'], usage='calculation'):
    # usage either 'visualization' or 'calculation'
    day = int(date.strftime('%j'))
    hour = date.hour
    minute = date.minute

    grid_id = query_db('SELECT GridID FROM Date WHERE DAY = ? AND Hour = ? AND Minute = ?', [day, hour, minute])
    if not grid_id:
        grid_id = 0

    graph = {}
    nodes = {}
    try:
        for node in query_db('SELECT * FROM Nodes'):
            nodes[node[0]] = (node[1], node[2])
    except sqlite3.Error as e:
        print 'SQL-Error: Not able to load <Nodes> from Database'
        print e.message
    try:
        if usage == 'visualization':
            edges = query_db('SELECT FromID, ToID, Factor FROM Graph WHERE GridID = ?', [grid_id])
        else:
            edges = query_db('SELECT FromID, ToID, Costs FROM Graph WHERE GridID = ?', [grid_id])
        for edge in edges:
            start = edge[0]
            end = edge[1]
            cost = edge[2]
            if not graph.get(start):
                graph[start] = {end: cost}
            else:
                graph[start][end] = cost
    except sqlite3.Error as e:
        print 'SQL-Error: Not able to load <Edges> from Database'
        print e.message
    return graph, nodes

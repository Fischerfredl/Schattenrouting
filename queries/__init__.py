import sqlite3
from config import config


def query_db(query, args=()):
    connection = sqlite3.connect(config['DATABASE'])
    cur = connection.cursor().execute(query, args)
    return cur.fetchall()


def get_bounds():
    try:
        bounds = {}
        north, south, west, east = query_db('SELECT MAX(Lat_m), MIN(Lat_m), MIN(Lon_m), MAX(Lon_m) FROM Gebaeude')[0]
        bounds['north'] = north + 0.002
        bounds['south'] = south - 0.002
        bounds['east'] = east + 0.006
        bounds['west'] = west - 0.003
    except sqlite3.Error as e:
        print 'SQL-Error: Load default values for <Bounds>'
        print e.message
        return config['DEFAULT_BOUNDS']
    return bounds


def get_max_height():
    height = 30
    try:
        height = query_db('SELECT MAX(Gebaeudehoehe) FROM Gebaeude')[0][0]
    except sqlite3.Error as e:
        print 'SQL-Error: Load default value for <Building-Max-Height>'
    return height


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
    try:
        return query_db('SELECT * FROM Gebaeude')
    except sqlite3.Error as e:
        print 'SQL-Error: Not able to load <Gebaeude> from Database'
        print e.message
        return False


def get_edges():
    try:
        return query_db('SELECT * FROM Edges')
    except sqlite3.Error as e:
        print 'SQL-Error: Not able to load <Edges> from Database'
        print e.message
        print False


def get_graph():
    graph = {}
    nodes = {}
    try:
        nodes = {}
        for node in query_db('SELECT * FROM Nodes'):
            nodes[node[0]] = (node[1], node[2])
    except sqlite3.Error as e:
        print 'SQL-Error: Not able to load <Nodes> from Database'
        print e.message
    try:
        for edge in query_db('SELECT * FROM Edges'):
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

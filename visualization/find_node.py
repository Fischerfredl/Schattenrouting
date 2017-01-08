import numpy as np
from queries import get_nodes


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

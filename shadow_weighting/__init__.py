from flask import session
import numpy as np
from queries import get_buildings, get_graph, get_max_height
from data.kml_coordinates import coords_to_array
from calculation import get_solar_position, get_shadow_vektor


def in_rectangle(point, rect):
    return True


def narrowed_rectangle(start, end, angle, length):
    narrowed = [start, end]
    # angle transformation
    angle = 360 - (angle + 90)
    # calculate vektor in lon-lat difference
    vektor = ((np.sin(angle)*length*const)*111.3, (np.cos(angle)*length*const)*111.3*np.cos(start[0]*const))
    narrowed.append(end+vektor)
    narrowed.append(start+vektor)
    return narrowed


def narrowed_buildings(start, end):
    rect = narrowed_rectangle(start, end, angle, length)
    buildings = []
    for bldg in get_buildings():
        for point in coords_to_array(bldg[5]):
            if in_rectangle(point, rect):
                buildings.append(bldg)
                break
    return buildings


def shadow_weighting():
    graph, nodes = get_graph()
    buildings = get_buildings()
    bldg_heigth_max = get_max_height()

    azimut, elevation = get_solar_position(session['date'], session['start'])
    get_shadow_vektor(azimut, elevation, bldg_heigth_max)


    return
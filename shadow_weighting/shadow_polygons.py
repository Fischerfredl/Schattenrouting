from shapely import speedups
from shapely.geometry import Polygon
from shapely.ops import unary_union
from datetime import datetime
from solar_position import get_solar_position
import numpy as np
from queries import get_buildings

const = np.pi / 180
speedups.enable()


def transform_point(point, azimut, length):
    delta_lat = np.cos(const*azimut)*length*0.001
    delta_lon = np.sin(const*azimut)*length*0.001
    vektor = (delta_lat/111.3, delta_lon/(111.3*np.cos(const*point[0])))
    return point[0]-vektor[0], point[1]-vektor[1]


def coords_to_array(coords):
    coord_array = []
    for c in coords.strip().split(';'):
        x, y = c.split(',')
        coord_array.append((float(x), float(y)))
    return coord_array


def building_shadow(building, azimut, elevation):
    polygons = []
    coords = coords_to_array(building[5])
    height = building[4]
    length = height / np.tan(const * elevation)
    for i, item in enumerate(coords[1:], start=1):
        poly = [coords[i - 1],
                coords[i],
                transform_point(coords[i], azimut, length),
                transform_point(coords[i - 1], azimut, length)]
        polygons.append(Polygon(poly))
    polygons.append(Polygon(coords))
    return unary_union(polygons)


def get_shadow_polygons():

    azimut, elevation = get_solar_position(datetime(2007, 12, 20, 8, 30))
    print elevation
    i = 1
    polygons = []
    for bldg in get_buildings():
        polygons.append(building_shadow(bldg, azimut, elevation))
        i += 1

    union = unary_union(polygons)

    if union.geom_type == 'Polygon':
        shadow_polys = [list(union.exterior.coords)]
    elif union.geom_type == 'MultiPolygon':
        shadow_polys = [list(p.exterior.coords) for p in unary_union(polygons)]
    else:
        shadow_polys = []

    return shadow_polys

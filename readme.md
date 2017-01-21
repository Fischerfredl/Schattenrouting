Schattenrouting
App zur Berechnung der Schattigsten Route zwischen zwei Punkten

Packages:
config              Contains Configuration for the Server such as Database Location
data                Extract Raw Data from Openstreetmap(OSM) or KML-File and parse into database
external            External python packages. (Dijkstra, Priodict, Momentjs)
parameters          Maintains session wide parameters. Updates on every request. Handles data formats
queries             Functions to retrieve data from database
visualization       Creates Map and Map Objects (Bounds-Rectangle, Graph-Polylines, Buildings-Polygons, Markers und Routes)


Dependencies:
python 2.7
flask
flask-googlemaps
geopy

The Website/Webapp contains a Map provided by Google Maps.
You can Toggle different Map-Objects.
-Rectangle: A Rectangle showing the bounds used for navigation.
-Buildings: Plots layout of the buildings as Polygons.
-Graph: Shows the graph used for routing. Can be used for locating unconnected nodes.
-Nodes: Shows all nodes. Nodes are clickable und can be used for setting waypoints.
-Shortest Path: Shows the Shortest Path between start- and end-node
ToDo: -Shadiest Path: Shows the shadiest path between start- and end-node

Warning: Graph, Buildings and Nodes have heavy influence on loading times. Showing all at once may take a few seconds to load. Operability is slightly influenced. (Only tested on my machine locally)
Warning: Graph, Buildings and Nodes have severe influence on loading times and operapility on mobile phone. (Only tested on my mobile phone in local network)

Coordinates can be set by entering any kind of Address in the Coordinates-Fields. The Address will be geocoded.
The coordinates are automatically transferred into the bounds-rectangle if the user provided coordinates out of bounds.
ToDo: Mobile: set start by GPS-Module

The date which is used for calculation of the shadiest route will be reset to present time every refresh.
When a different date is set it will only be used for the next request.



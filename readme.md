Schattenrouting

App zur Berechnung der Schattigsten Route zwischen zwei Punkten.
Calculating the shadiest path between two points.


Dependencies:

python 2.7

flask

geopy


The Website/Webapp contains a Map provided by Google Maps.


You can Toggle different Map-Objects:

-Buildings: Plots layout of the buildings as Polygons.

-Graph: Shows the graph used for routing. Can be used for locating unconnected nodes.

-Shadows: Shows the Shadows thrown by buildings

-Paths: Shows the shortest/shadiest/sunniest Path between start- and end-node


Coordinates can be set dragging the Markers or by entering any kind of Address in the Location-Fields. The Address will be geocoded.


Warning: Graph, Buildings and Shadows are data heavy and have influence on loading times. Showing all at once may take a few seconds to load. Operability is slightly influenced. (Only tested on my machine locally)

Warning: Graph, Buildings and Nodes have severe influence on loading times and operapility on mobile phone. (Only tested on my mobile phone in local network)

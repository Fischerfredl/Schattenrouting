// map
var map;

// bounds
var rect = null;

// coordinates
var start = null;
var end = null;
var start_addr = null;
var end_addr = null;

// date
var date = null;
var time = null;

// solar position
var azimut = null;
var elevation = null;

// paths
var shortest = null;
var shadiest = null;
var sunniest = null;

// data
var bldg = [];
var graph = [];
var shadows = [];

// for infoboxes
var prev_infowindow_map = null;


function initialize() {
    //noinspection JSUnresolvedVariable,JSUnresolvedFunction
    map = new google.maps.Map(
        document.getElementById('map'),
        {
            center: {lat: 48.3645044, lng: 10.8891771},
            zoom: 14,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            zoomControl: true,
            mapTypeControl: true,
            scaleControl: true,
            streetViewControl: false,
            rotateControl: true,
            scrollwheel: true,
            fullscreenControl: false
        });

    init_start();
    init_end();
    set_address();
    init_date();
    set_solar_position();
    init_rect();
    load_path();
    refresh();


// ---------------------------------------------------------------------------------------------------------------------
// initialize functions
// ---------------------------------------------------------------------------------------------------------------------

    function init_start() {
        // !!!!!add: get position from device!!!!!
        //noinspection JSUnresolvedVariable,JSUnresolvedFunction
        start = new google.maps.Marker({
            position: new google.maps.LatLng(48.3645044, 10.8891771),
            map: map,
            label: 'A',
            draggable: true
        });
        //noinspection JSUnresolvedVariable
        google.maps.event.addListener(start, 'click', getInfoCallback(map, 'From'));
    }

    function init_end() {
        //noinspection JSUnresolvedVariable,JSUnresolvedFunction
        end = new google.maps.Marker({
            position: new google.maps.LatLng(48.3709503, 10.9091661),
            map: map,
            label: 'B',
            draggable: true
        });
        //noinspection JSUnresolvedVariable
        google.maps.event.addListener(end, 'click', getInfoCallback(map, 'To'));
    }

    function init_date() {
        date = moment().format('YYYY-MM-DD');
        time = moment().format('HH:mm');
    }

    function init_rect() {
        $.getJSON($SCRIPT_ROOT + '/api/get_bounds', {}, function (data) {
            //noinspection JSUnresolvedVariable,JSUnresolvedFunction
            rect = new google.maps.Rectangle({
                strokeColor: '#00603F',
                strokeOpacity: 1.,
                strokeWeight: 4,
                fillColor: '#FFFFFF',
                fillOpacity: .1,
                map: map,
                bounds: {
                    north: data.north,
                    east: data.east,
                    south: data.south,
                    west: data.west
                }
            });
        });
    }

// ---------------------------------------------------------------------------------------------------------------------
// after data change
// ---------------------------------------------------------------------------------------------------------------------

    function set_address() {
        $.getJSON(
            $SCRIPT_ROOT + '/api/reverse_geocode',
            {startlat: start.lat, startlon: start.lng, endlat: end.lat, endlon: end.lng},
            function (data) {
                if (data.start_addr) start_addr = data.start_addr;
                if (data.end_addr) end_addr = data.end_addr
            });
    }

    function set_solar_position() {
        $.getJSON(
            $SCRIPT_ROOT + '/api/get_solar_position',
            {date: date, time: time},
            function (data) {
                if (data.azimut) azimut = data.azimut;
                if (data.elevation) elevation = data.elevation
            });
    }

    function refresh() {
        // !!!!!add: update html elements!!!!!
        document.getElementById("input_date").value = date;
        document.getElementById("input_time").value = time;
    }

// ---------------------------------------------------------------------------------------------------------------------
// data change triggers
// ---------------------------------------------------------------------------------------------------------------------


//noinspection JSUnresolvedVariable
    google.maps.event.addListener(start, 'dragend', function () {
        set_address();
        load_path();
        refresh();
    });

//noinspection JSUnresolvedVariable
    google.maps.event.addListener(end, 'dragend', function () {
        set_address();
        load_path();
        refresh();
    });

    function set_location() {
        $.getJSON(
            $SCRIPT_ROOT + '/api/geocode',
            {start: document.getElementById('set_coords_start').value, end: document.getElementById('set_coords_end')},
            function (data) {
                if (data.start) {
                    start.lat = data.start[0];
                    start.lng = data.start[1];
                }
                if (data.end) {
                    end.lat = data.end[0];
                    end.lng = data.end[1];
                }
            });
        set_address();
        load_path();
        refresh();
    }

    function set_date() {
        date = document.getElementById('input_date').value;
        time = document.getElementById('input_time').value;
        if (bldg.length != 0) {
            if (bldg[0].map != null) load_buildings();
            else bldg = [];
        }
        if (shadows.length != 0) {
            if (shadows[0].map != null) load_shadows();
            else shadows = [];
        }
        if (graph.length != 0) {
            if (graph[0].map != null) load_graph();
            else graph = [];
        }
        load_path();
    }

// ---------------------------------------------------------------------------------------------------------------------
// toggles
// ---------------------------------------------------------------------------------------------------------------------


    function toggle_bldg() {
        if (bldg.length == 0 ) load_buildings();
        else if (bldg[0].map == null) for (var i in bldg) bldg[i].setMap(map);
        else for (var j in bldg) bldg[j].setMap(null)
    }

    function toggle_routes() {
        if (graph.length == 0) load_graph();
        else if (graph[0].map == null) for (var i in graph) graph[i].setMap(map);
        else for (var j in graph) graph[j].setMap(null)
    }

    function toggle_shadows() {
        if (shadows.length == 0) load_shadows();
        else if (shadows[0].map == null) for (var i in shadows) shadows[i].setMap(map);
        else for (var j in shadows) shadows[j].setMap(null)
    }

    function toggle_shortest() {
        if (shortest.map == null) shortest.setMap(map);
        else shortest.setMap(null)
    }

    function toggle_shadiest() {
        if (shadiest.map == null) shadiest.setMap(map);
        else shadiest.setMap(null)
    }

    function toggle_sunniest() {
        if (sunniest.map == null) sunniest.setMap(map);
        else sunniest.setMap(null)
    }

// ---------------------------------------------------------------------------------------------------------------------
// load data
// ---------------------------------------------------------------------------------------------------------------------

    function load_path() {
        if (shortest != null) shortest.setMap(null);
        if (shadiest != null) shadiest.setMap(null);
        if (sunniest != null) sunniest.setMap(null);

        // shortest
        $.getJSON(
            $SCRIPT_ROOT + '/api/get_path',
            {
                date: date,
                time: time,
                startlat: start.getPosition().lat(),
                startlon: start.getPosition().lng(),
                endlat: end.getPosition().lat(),
                endlon: end.getPosition().lng(),
                pathtype: "shortest"
            },
            function (data) {
                //noinspection JSUnresolvedVariable,JSUnresolvedFunction
                shortest = new google.maps.Polyline({
                    strokeColor: '#00B3FD',
                    strokeOpacity: 0.9,
                    strokeWeight: 5,
                    path: data,
                    map: null,
                    geodesic: true
                });
            });
        // shadiest
        $.getJSON(
            $SCRIPT_ROOT + '/api/get_path',
            {
                date: date,
                time: time,
                startlat: start.getPosition().lat(),
                startlon: start.getPosition().lng(),
                endlat: end.getPosition().lat(),
                endlon: end.getPosition().lng(),
                pathtype: "shadiest"
            },
            function (data) {
                //noinspection JSUnresolvedVariable,JSUnresolvedFunction
                shadiest = new google.maps.Polyline({
                    strokeColor: '#005071',
                    strokeOpacity: 0.9,
                    strokeWeight: 5,
                    path: data,
                    map: map,
                    geodesic: true
                });
            });
        // sunniest
        $.getJSON(
            $SCRIPT_ROOT + '/api/get_path',
            {
                date: date,
                time: time,
                startlat: start.getPosition().lat(),
                startlon: start.getPosition().lng(),
                endlat: end.getPosition().lat(),
                endlon: end.getPosition().lng(),
                pathtype: "sunniest"
            },
            function (data) {
                //noinspection JSUnresolvedVariable,JSUnresolvedFunction
                sunniest = new google.maps.Polyline({
                    strokeColor: '#dfd414',
                    strokeOpacity: 0.9,
                    strokeWeight: 5,
                    path: data,
                    map: null,
                    geodesic: true
                });
            });

    }

    function load_buildings() {
        $.getJSON($SCRIPT_ROOT + '/api/get_buildings', {}, function (data) {
            for (var i = 0; i < data.length; i++) {
                //noinspection JSUnresolvedVariable,JSUnresolvedFunction
                bldg[i] = new google.maps.Polygon({
                    strokeColor: '#00603F',
                    strokeOpacity: 0.7,
                    strokeWeight: 1,
                    fillOpacity: .5,
                    fillColor: '#53c49d',
                    path: data[i],
                    map: map,
                    geodesic: true
                });
            }
        });
    }

    function load_shadows() {
        $.getJSON($SCRIPT_ROOT + '/api/get_shadows', {date: date, time: time}, function (data) {
            for (var i = 0; i < data.length; i++) {
                //noinspection JSUnresolvedVariable,JSUnresolvedFunction
                shadows[i] = new google.maps.Polygon({
                    strokeColor: '#808080',
                    strokeOpacity: 0.7,
                    strokeWeight: 1,
                    fillOpacity: .5,
                    fillColor: '#808080',
                    map: map,
                    path: data[i],
                    geodesic: true
                });
            }
        });


    }

    function load_graph() {
        $.getJSON($SCRIPT_ROOT + '/api/get_graph', {date: date, time: time}, function (data) {
            for (var i = 0; i < data.length; i++) {
                //noinspection JSUnresolvedVariable,JSUnresolvedFunction
                graph[i] = new google.maps.Polyline({
                    strokeColor: data[i][2],
                    strokeOpacity: 0.9,
                    strokeWeight: 3,
                    map: map,
                    path: [data[i][0], data[i][1]],
                    geodesic: true
                });
            }
        });
    }

// ---------------------------------------------------------------------------------------------------------------------
// for infobox
// ---------------------------------------------------------------------------------------------------------------------

    function getInfoCallback(map, content) {
        //noinspection JSUnresolvedVariable,JSUnresolvedFunction
        var infowindow = new google.maps.InfoWindow({content: content});
        return function (ev) {
            if (prev_infowindow_map) {
                prev_infowindow_map.close();
            }
            prev_infowindow_map = infowindow;
            //noinspection JSUnresolvedFunction,JSUnresolvedVariable
            infowindow.setPosition(ev.latLng);
            //noinspection JSUnresolvedFunction
            infowindow.setContent(content);
            infowindow.open(map, this);
        };
    }

    document.getElementById("toggle_shortest").onclick = toggle_shortest;
    document.getElementById("toggle_shadiest").onclick = toggle_shadiest;
    document.getElementById("toggle_sunniest").onclick = toggle_sunniest;
    document.getElementById("toggle_bldg").onclick = toggle_bldg;
    document.getElementById("toggle_routes").onclick = toggle_routes;
    document.getElementById("toggle_shadows").onclick = toggle_shadows;

    document.getElementById("set_coords").onclick = set_location;
    document.getElementById("set_date").onclick = set_date;

}

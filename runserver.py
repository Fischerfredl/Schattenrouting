from flask import Flask, render_template, request, jsonify
from queries import get_bounds, get_buildings, get_graph_visualization, get_shadow, get_graph, get_solar_position
from datetime import datetime
from external.secret_key import get_secret_key
from geocoding import geolocate_coords, geolocate_query

app = Flask(__name__)
app.config['SECRET_KEY'] = get_secret_key()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/api/get_bounds')
def api_get_bounds():
    return jsonify(get_bounds())


@app.route('/api/get_buildings')
def api_get_buildings():
    return jsonify(get_buildings())


@app.route('/api/get_graph')
def api_get_graph():
    date = request.args.get('date', None, str)
    time = request.args.get('time', None, str)
    lines = get_graph_visualization(datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M'))
    return jsonify(lines)


@app.route('/api/get_shadows')
def api_get_shadows():
    date = request.args.get('date', None, str)
    time = request.args.get('time', None, str)
    polygons = get_shadow(datetime.strptime(date+' '+time, '%Y-%m-%d %H:%M'))
    return jsonify(polygons)


@app.route('/api/get_path')
def api_get_path():
    date = request.args.get('date', None, str)
    time = request.args.get('time', None, str)
    start_lat = request.args.get('startlat', None, float)
    start_lon = request.args.get('startlon', None, float)
    end_lat = request.args.get('endlat', None, float)
    end_lon = request.args.get('endlon', None, float)
    date = datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')
    path_shortest = get_graph(date, (start_lat, start_lon), (end_lat, end_lon), case='shortest')
    path_shadiest = get_graph(date, (start_lat, start_lon), (end_lat, end_lon), case='shadiest')
    path_sunniest = get_graph(date, (start_lat, start_lon), (end_lat, end_lon), case='sunniest')
    return jsonify({'shortest': path_shortest, 'shadiest': path_shadiest, 'sunniest': path_sunniest})


@app.route('/api/geocode')
def geocode():
    start_str = request.args.get('start_str', None, str)
    end_str = request.args.get('end_str', None, str)
    return jsonify({'start': geolocate_query(start_str), 'end': geolocate_query(end_str)})


@app.route('/api/reverse_geocode')
def reverse_geocode():
    lat = request.args.get('lat', None, float)
    lon = request.args.get('lon', None, float)
    return jsonify({'address': geolocate_coords((lat, lon))})


@app.route('/api/get_solar_position')
def solar_position():
    date = request.args.get('date', None, str)
    time = request.args.get('time', None, str)
    az, el = get_solar_position(datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M'))
    return jsonify({'azimut': az, 'elevation': el})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

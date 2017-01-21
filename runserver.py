from flask import Flask, render_template, request, jsonify
from parameters import init, process_post
from queries import get_bounds, get_buildings, get_graph_visualization, get_shadow, get_graph
from datetime import datetime
from external.secret_key import get_secret_key

app = Flask(__name__)
app.config['SECRET_KEY'] = get_secret_key()


@app.route('/', methods=['GET', 'POST'])
def index():
    init()
    if request.method == 'POST':
        process_post()
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
    path_type = request.args.get('pathtype', None, str)
    path = get_graph(datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M'),
                     (start_lat, start_lon), (end_lat, end_lon), case=path_type)
    return jsonify(path)


@app.route('/api/geocode')
def geocode():
    return jsonify({'dummy': 0})


@app.route('/api/reverse_geocode')
def reverse_geocode():
    return jsonify({'dummy': 0})


@app.route('/api/get_solar_position')
def solar_position():
    return jsonify({'dummy': 0})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, threaded=True)

from flask import Flask, render_template, request, session
from flask_googlemaps import GoogleMaps
from config import set_config
from parameters import init, process_post
from visualization import build_map

app = Flask(__name__)
set_config(app)
GoogleMaps(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    init()
    if request.method == 'POST':
        process_post()
    mymap = build_map()
    return render_template('index.html', mymap=mymap)

if __name__ == "__main__":
    app.run(host=app.config['IPADDR'], port=app.config['PORT'], threaded=True)

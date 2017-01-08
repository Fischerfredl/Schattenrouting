from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from data import parse_to_database
from config import set_config
from external.momentjs import momentjs
from parameters import init, process_post
from visualization import build_map

app = Flask(__name__)
set_config(app)
GoogleMaps(app)
app.jinja_env.globals['momentjs'] = momentjs

assert(parse_to_database() is not False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        process_post()
    init()
    mymap = build_map()
    return render_template('index.html', mymap=mymap)

if __name__ == "__main__":
    app.run(host=app.config['IPADDR'], port=app.config['PORT'])

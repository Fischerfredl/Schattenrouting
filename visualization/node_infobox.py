from flask import url_for


def html(lat, lon):
    return '<b>A simple node</b>' \
           '<br>' \
           '<a href="'+url_for('index', start=str(lat)+','+str(lon))+'">Route from here</a>' \
           '<br>' \
           '<a href="'+url_for('index', end=str(lat)+','+str(lon))+'">Route to here</a>'

"""
Author: Marissa Mocenigo

This class interacts with the web components

"""

import logging

from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps, Map
from source.user_location import get_user_info, get_location_data, where_am_i
from config import GOOGLE_API_KEY
from source.activity_manager import plan_hours

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the Flask application
app = Flask(__name__)
app.config['GOOGLEMAPS_KEY'] = GOOGLE_API_KEY
GoogleMaps(app)

@app.route('/')
def index():
    user_info = get_user_info()
    return render_template('index.html', user_info=user_info)

@app.route('/suggestions', methods=['POST'])
def request_itinerary():
    hours = request.form['hours']
    location = get_location_data()
    latlong = str(location['latitude']) + "," + str(location['longitude'])
    activities = plan_hours(latlong, float(hours), [])
    if len(activities) > 0:
        markers = []# [(a["lat"], a["lng"]) for a in activities]
        for a in activities:
            m = {
             'lat': a["lat"],
             'lng': a["lng"],
             'infobox': a["name"]
          }
            markers.append(m)
        map = Map(
                identifier="view-side",
                lat=location['latitude'],
                lng=location['longitude'],
                markers=markers,
                style = "height:500px;width:100%;margin:5px;"
            )
        return render_template('suggestion.html', hours=hours, activities=activities, map=map)
    else:
        render_template('suggestion.html', hours=hours)

if __name__ == '__main__':
    app.run()


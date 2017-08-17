import pyowm, requests, json, pytz
from datetime import datetime
from config import WEATHER_API_KEY

owm = pyowm.OWM(WEATHER_API_KEY)

def get_user_info():
    user_info = {}
    my_loc = get_location_data()
    user_info['location'] = where_am_i(my_loc)
    user_info['weather_desc'] = get_weather_condition(my_loc)
    user_info['latitude'] = my_loc['latitude']
    user_info['longitude'] = my_loc['longitude']
    user_info['current_time'] = get_current_time(my_loc)
    return user_info

def get_current_time(my_loc):
    zone = pytz.timezone(my_loc['time_zone'])
    loc_time = datetime.now(zone)
    return loc_time.strftime("%I:%M %p %Z")

def where_am_i(my_loc):
    if my_loc['country_code'] is 'US':
        return my_loc['city'] + ', ' + my_loc['region_name']
    else:
        return my_loc['city'] + ', ' + my_loc['country_name']

def lat_lng_str():
    d = get_location_data()
    return str(d['latitude']) + "," + str(d['longitude'])

def get_location_data():
    r = requests.get("http://freegeoip.net/json")
    pos = json.loads(r.text)
    return pos

def get_current_weather(my_loc):
    my_weather = owm.weather_at_coords(my_loc['latitude'], my_loc['longitude'])
    temp = my_weather.get_weather().get_temperature(unit='celsius')['temp']
    return my_weather.get_weather()

def get_weather_condition(my_loc):
    weather = get_current_weather(my_loc)
    return weather.get_detailed_status().lower()
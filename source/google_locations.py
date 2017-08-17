import requests, json
from random import randint
from config import GOOGLE_API_KEY, MAPS_SEARCH_URL, PLACE_DETAILS_URL, TRAVEL_TIME_URL, PHOTO_URL

def get_nearby(latlng, type, opennow=True):
    params = {
        "key": GOOGLE_API_KEY,
        "location" : latlng,
        "radius": 1800,
        "type" : type,
        "opennow": "true" if opennow else "false"
    }
    req = requests.get(MAPS_SEARCH_URL, params=params)
    # Dump the JSON object into an element
    jdata = json.dumps(req.json())
    # Load to a string
    resp = json.loads(jdata)
    # How many matches did we find?
    num_places = len(resp["results"])
    if num_places > 0:
        # Choose one at random and return the place id
        return resp["results"][randint(0, num_places - 1)]["place_id"]
    else:
        return None


def get_place_details(place_id):
    params = {
        "key": GOOGLE_API_KEY,
        "placeid": place_id
    }
    req = requests.get(PLACE_DETAILS_URL, params=params)
    res = req.json()
    # Dump the JSON object into an element
    jdata = json.dumps(req.json())
    # Load to a string
    resp = json.loads(jdata)["result"]
    place_details = {
    "name": resp["name"],
    "address": resp["formatted_address"],
    "link": resp["website"] if "website" in resp else "",
    "lat": resp["geometry"]["location"]["lat"],
    "lng": resp["geometry"]["location"]["lng"]
    }
    return place_details

def get_matching_place(latlng, type):
    place_id = get_nearby(latlng, type)
    if place_id:
        return get_place_details(place_id)
    else:
        return None

def get_travel_time(origin, destination):
    params = {
        "key": GOOGLE_API_KEY,
        "origins": origin,
        "destinations": destination,
        "mode": "walking"
    }
    req = requests.get(TRAVEL_TIME_URL, params=params)
    res = req.json()
    return convert_duration_str_to_hours(res["rows"][0]["elements"][0]["duration"]["text"])

def convert_duration_str_to_hours(duration):
    parts = duration.split(" ")
    prev = ""
    hours = 0
    for p in parts:
        if p == "days" or p == "day":
            hours += float(prev)*24
        if p == "hours" or p == "hour":
            hours += float(prev)
        if p == "mins" or p == "min":
            hours += float(prev)/60
        else:
            prev = p
    return hours
import google_locations
import logging
from db import get_location_type

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Just putting these here for readability
TYPE_NAME = 0
TYPE_DURATION = 1

def plan_hours(latlng, num_hours, activities = [], retry = 0):
    logging.info("Picking an activity...")
    if retry > 3 or num_hours < 0.5:
        # The smallest unit of time we can allocate is 0.5
        # If we couldn't find a match after 3 tries, return whatever we could find
        return activities
    # Location types (cafe, museum, etc) are coded with an expected time
    # We choose an activity that is smaller than the number of hours we need to fill
    # type_info is both the 'type' name and an estimated duration
    type_info = get_location_type(num_hours)
    # Get the first place returned by Google that matches our criteria
    place_details = google_locations.get_matching_place(latlng, type_info[TYPE_NAME])
    if place_details:
        # Make the type a bit human readable
        place_details["type"] = type_info[TYPE_NAME].replace("_", " ").title()
        # Add the place details
        activities.append(place_details)
        # Reduce the number of hours we have to fill by the duration of the chosen activity
        num_hours -= float(type_info[TYPE_DURATION])
        # Now, we start from this point as our origin
        new_latlng = str(place_details["lat"]) + "," + str(place_details["lng"])
        # Calculate walking distance between both
        travel_time = google_locations.get_travel_time(latlng, new_latlng)
        # Reduce our overall activity time by the walking time
        num_hours -= travel_time
        # And start from the new location
        latlng = str(place_details["lat"]) + "," + str(place_details["lng"])
    else:
        retry += 1
    return plan_hours(latlng, num_hours, activities, retry)


from source.google_locations import get_nearby, get_place_details, convert_duration_str_to_hours


def test_get_nearby():
    test_latlng = "52.520007,13.404954"
    type = "cafe"
    res = get_nearby(test_latlng, type, False)
    assert(res is not None)

def test_get_place_details():
    placeid = "ChIJJyRIGsNRqEcR_Ft77KRW8SM"
    det = get_place_details(placeid)
    assert(det['name'] == 'LE CROBAG')

    52.52174109999999,13.4111594

def test_time_conversion():
    day = '1 day'
    day_hrs = convert_duration_str_to_hours(day)
    assert(day_hrs == 24)
    two_days = '2 days'
    days_hrs = convert_duration_str_to_hours(two_days)
    assert(days_hrs == 48)
    hour = '1 hour'
    hr = convert_duration_str_to_hours(hour)
    assert(hr == 1)
    half_hour = '30 mins'
    hf = convert_duration_str_to_hours(half_hour)
    assert(hf == 0.5)
    mixed_time = '2 hours 30 mins'
    mix = convert_duration_str_to_hours(mixed_time)
    assert(mix == 2.5)
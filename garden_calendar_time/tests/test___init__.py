import garden_calendar_time

def test_LatLong_smoketest():
    LatLong = garden_calendar_time.LatLong

    loc = LatLong(45, 45)
    assert loc.lat == 45
    assert loc.long == 45

    loc = LatLong(-45, -45)
    assert loc.lat == -45
    assert loc.long == -45

    loc = LatLong(135, 135)
    assert loc.lat == 45
    assert loc.long == 135

    loc = LatLong(-135, -135)
    assert loc.lat == -45
    assert loc.long == -135

    loc = LatLong(90, 180)
    assert loc.lat == 90
    assert loc.long == 180

    loc = LatLong(-90, -180)
    assert loc.lat == -90
    assert loc.long == 180

    loc = LatLong(180, 360)
    assert loc.lat == 0
    assert loc.long == 0
